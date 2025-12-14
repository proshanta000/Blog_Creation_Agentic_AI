from src.Blog_Post_AI_Agent.states.blogstate import BlogState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.Blog_Post_AI_Agent.states.blogstate import Blog
from typing import Dict, Any


class BlogNode:
    """
    A class to represent the blog node
    """

    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state:BlogState):
        """
        Create the title for the blog
        """

        if "topic" in state and state["topic"]:
            prompt="""
                        You are an expert blog content writer. Use Markdown formatting. Generate
                        a blog title for the {topic}. This title should be creative and SEO friendly.
                    """
            
            system_messages = prompt.format(topic = state["topic"])
            response = self.llm.invoke(system_messages)
            return {"blog": {"title": response.content}}
        

    def content_generation(self, state:BlogState):
        """
        Create the content for the blog
        """

        if "topic" in state and state["topic"]:
            system_prompt="""
                        You are an expert blog content writer. Use Markdown formatting. Generate
                        a detailed blog content with detailed breakdown for the {topic}.
                    """
            
            system_messages = system_prompt.format(topic = state["topic"])
            response = self.llm.invoke(system_messages)
            return {"blog": {"title": state['blog']['title'], 'content': response.content}}
        
    


    def translation(self, state: BlogState):
            """ 
            Translate the content to the specific language.
            """
            
            # NOTE: Fixed typo from 'translate_ptompt' to 'translate_prompt'
            translate_prompt = """
            Translate the following content into {current_language}.
            - Maintain the original tone, style , and formatting.
            - Adapt cultural references and idioms  to be appropriate for {current_language}
            - IMPORTANT: Only return the translated text content, nothing else.

            ORIGINAL CONTENT :
            {blog_content}
            
            """

            blog_content = state["blog"]["content"]
            current_language = state["current_language"]
            
            messages = [
                HumanMessage(translate_prompt.format(current_language=current_language, blog_content=blog_content))
            ]

            # 🛑 CRITICAL FIX: Use standard invoke() to return raw text
            translated_response = self.llm.invoke(messages)
            translated_content = translated_response.content
            
            # Determine the correct key for the translated content (e.g., 'content_bangla')
            state_key = f"content_{current_language.lower()}"

            # Update the state with the new content while keeping the title
            return {
                "blog": {
                    "title": state['blog']['title'],
                    "content": state['blog']['content'], # Keep English version
                    state_key: translated_content       # Add translated version
                }
            }
    

    



    def format_output(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Selects the final translated content, formats the blog post,
        and prepares the final state object.
        """
        print("--- Running format_output Node ---")

        output_language = state.get("current_language", "english").lower()
        blog_data = state.get("blog", {})
        title = blog_data.get("title", "Untitled Blog Post")
        
        # 1. Select the final content based on the target language
        # We look for the translated content key (e.g., 'content_bangla')
        content_key = f"content_{output_language}"
        final_content = blog_data.get(content_key)
        
        # Fallback to the original English content if translation failed/wasn't done
        if not final_content:
            final_content = blog_data.get("content", "Content generation or translation failed.")
            
        # 2. Structure the Final Result for consumption
        final_blog_post = {
            "title": title,
            "language": output_language,
            "content": final_content,
            "status": "Ready for Publishing"
        }
        
        # 3. Return the Final Update
        # We return the structured final post and a status message.
        return {
            "final_post": final_blog_post,
            "status_message": f"Blog post successfully generated and formatted in {output_language.upper()}."
        }