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

            
            translated_response = self.llm.invoke(messages)
            translated_content = translated_response.content
            
            # Determine the correct key for the translated content (e.g., 'content_bangla')
            state_key = f"content_{state['current_language'].lower()}"

            # Create a copy of the existing 'blog' dictionary
            updated_blog = state['blog'].copy()
            # Add the new translated content to the 'blog' dictionary
            updated_blog[state_key] = translated_content
            
            
            # Return the updated state
            return {
                "translated_content": translated_content
            }
    

    



    def format_output(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Selects the final content, formats the blog post,
        and prepares the final state object for the consumer (FastAPI).
        """
        print("--- Running format_output Node ---")

        output_language = state.get("current_language", "english").lower()
        blog_data = state.get("blog", {})
        title = blog_data.get("title", "Untitled Blog Post")
        
        # Default to English content
        final_content = blog_data.get("content", "Error: Content generation failed.")

        # If language is NOT English, we try to grab the translated content
        if output_language not in ["english", "en"]:
            # Check if translation node populated 'translated_content'
            translated_text = state.get("translated_content")
            if translated_text:
                final_content = translated_text
            else:
                # Fallback or error logging if needed
                print(f"Warning: No translated content found for {output_language}. Falling back to English.")
            
        # 2. Structure the Final Result for consumption 
        final_blog_post = {
            "title": title,
            "language": output_language,
            "content": final_content,
            "status": "Ready for Publishing"
        }
        
        # 3. Return the Final Update with the EXACT KEY the frontend expects: "final_post"
        return {
            "final_post": final_blog_post, 
            "status_message": f"Blog post successfully generated and formatted in {output_language.upper()}."
        }
    
    
    def route_decision(self, state: Dict[str, Any]) -> str:
        """
        Decides the next step based on the requested language ('bangla' or 'hindi').
        Returns the key matching the conditional edge dictionary in GraphBuilder.
        """
        # Checks 'current_language' instead of 'language'
        language = state.get("current_language", "").lower()
        
        if language in ["bangla", "hindi"]:
            return language
        else:
            # This triggers the "__default__" edge in GraphBuilder
            return "__default__" 


    def route(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        This node ensures the 'current_language' is set in the state 
        before moving to translation or format_output.
        """
        # If we already have current_language in state (from app.py), use it.
        # Otherwise fallback to checking 'language' or default.
        language = state.get("current_language") or state.get("language", "")
        language = language.lower()

        # If still no language is specified, set it to 'english'
        if not language:
            language = "english"
            
        # Return the state update, setting the current_language
        return {"current_language": language}