from langgraph.graph import StateGraph, START, END
from src.Blog_Post_AI_Agent.states.blogstate import BlogState
from src.Blog_Post_AI_Agent.nodes.blognode import BlogNode


class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)

    def build_topic_graph(self):
        """
        Build a graph to generate blogs based on topic.
        """
        self.blog_node_obj = BlogNode(self.llm)

        # --- Nodes ---
        # Add the chatbot node to the graph
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation )
        self.graph.add_node("content_generation",self.blog_node_obj.content_generation )
        self.graph.add_node("format_output", self.blog_node_obj.format_output)

        # --- edge ---
        # Define the flow: Start -> Chatbot(Generating blog) -> End
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", "format_output")
        self.graph.add_edge("format_output", END)

        return self.graph
    
    def build_language_graph(self):
        """
        Build a graph for blog generation with inputs topic and language.
        """

        self.blog_node_obj = BlogNode(self.llm)
        
        # --- Nodes ----
        # Add the chatbot node to the graph
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation )
        self.graph.add_node("content_generation",self.blog_node_obj.content_generation )
        self.graph.add_node("bangla_translation", lambda state: self.blog_node_obj.translation({**state, "current_language": "bangla"}) )
        self.graph.add_node("hindi_translation", lambda state: self.blog_node_obj.translation({**state, "current_language": "hindi"}) )
        self.graph.add_node("route", self.blog_node_obj.route )
        self.graph.add_node("format_output", self.blog_node_obj.format_output)
        


        # --- edge ---
        # Define the flow: Start -> Chatbot(Generating blog)-> Translating (bangla, hindi) -> End
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", "route")
        self.graph.add_conditional_edges(
            "route",
            self.blog_node_obj.route_decision,
            {
                "bangla":"bangla_translation",
                "hindi":"hindi_translation",
                "__default__": "format_output"  
            }
        )

        #  Edges: Translation nodes should now go to format_output, then END.
        self.graph.add_edge("bangla_translation", "format_output")
        self.graph.add_edge("hindi_translation", "format_output") 
        self.graph.add_edge("format_output", END)

        return self.graph
    


    def setup_graph(self, usecase):
        if usecase =="topic":
            self.build_topic_graph()
        
        if usecase =="language":
            self.build_language_graph()
        
        return self.graph.compile()
    