#!/usr/bin/env python3
"""
LLM-Powered AI Chatbot using Google Gemini
A simple chatbot with streaming responses and conversation history
"""

import os
import sys
try:
    import google.generativeai as genai
except ImportError:
    print("Please install the Google Generative AI library:")
    print("pip install google-generativeai")
    sys.exit(1)


class AIChatbot:
    def __init__(self, api_key: str, system_prompt: str = None):
        """
        Initialize the chatbot with Google Gemini API
        
        Args:
            api_key: Your Google Gemini API key
            system_prompt: Optional system instructions for the chatbot
        """
        genai.configure(api_key=api_key)
        
        # Default system prompt if none provided
        if system_prompt is None:
            system_prompt = """You are a helpful AI assistant.
You provide clear, concise answers.
You are friendly and professional in your responses."""
        
        self.system_prompt = system_prompt
        
        # Initialize the model with system instructions
        self.model = genai.GenerativeModel(
            model_name='gemini-pro',
            generation_config={
                'temperature': 0.7,
                'top_p': 1,
                'top_k': 1,
                'max_output_tokens': 2048,
            }
        )
        
        # Start a chat session for conversation history
        self.chat = self.model.start_chat(history=[])
        
        # Add system prompt as the first message
        self._initialize_with_system_prompt()
    
    def _initialize_with_system_prompt(self):
        """Initialize the chat with system prompt"""
        # Send system prompt as first message
        initial_message = f"System Instructions: {self.system_prompt}\n\nPlease acknowledge these instructions briefly."
        response = self.chat.send_message(initial_message)
        # The system prompt is now part of the conversation history
    
    def send_message(self, message: str, stream: bool = True):
        """
        Send a message to the chatbot and get a response
        
        Args:
            message: User's message
            stream: Whether to stream the response (default: True)
        
        Returns:
            The chatbot's response
        """
        try:
            if stream:
                # Stream the response
                response = self.chat.send_message(message, stream=True)
                full_response = ""
                
                for chunk in response:
                    if chunk.text:
                        print(chunk.text, end='', flush=True)
                        full_response += chunk.text
                
                print()  # New line after streaming
                return full_response
            else:
                # Non-streaming response
                response = self.chat.send_message(message)
                return response.text
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_history(self):
        """Get the conversation history"""
        return self.chat.history
    
    def clear_history(self):
        """Clear conversation history and restart chat"""
        self.chat = self.model.start_chat(history=[])
        self._initialize_with_system_prompt()


def main():
    """Main function to run the chatbot"""
    print("=" * 60)
    print("LLM-Powered AI Chatbot (Google Gemini)")
    print("=" * 60)
    
    # Get API key
    api_key = os.environ.get('GEMINI_API_KEY')
    key_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gemini api key.txt')
    
    if not api_key:
        if os.path.exists(key_file):
            try:
                with open(key_file, 'r') as f:
                    api_key = f.read().strip()
                print("Loaded API key from 'gemini api key.txt'")
            except Exception as e:
                print(f"Error reading 'gemini api key.txt': {e}")
                
    if not api_key:
        print("\nNo API key found in environment variable GEMINI_API_KEY")
        api_key = input("Please enter your Google Gemini API key: ").strip()
        
        if not api_key:
            print("Error: API key is required!")
            sys.exit(1)
    
    # Define system prompt - customize this to create your own chatbot personality!
    system_prompt = """You are a Software Engineering mentor and educator.
Your name is CodeMentor.
You generally use clear, concise explanations with 2-4 sentences.
You love teaching through practical, real-world projects.
You believe the best way to learn programming is by building actual tools and utilities.
When suggesting learning resources, you prefer hands-on coding challenges over theoretical study.
You are encouraging and patient with learners of all levels."""
    
    # Alternative system prompts you can try:
    
    # Dad joke bot:
    # system_prompt = """You are a Dad.
    # You generally use only a few short sentences.
    # You like to tell Dad jokes.
    # You are supportive and encouraging."""
    
    # Coding Challenges bot (from the document):
    # system_prompt = """You are a Software Engineer.
    # Your name is John.
    # You generally use only a few sentences.
    # You write the website and newsletter Coding Challenges.
    # Coding Challenges are challenges that you've used or are using as exercises to
    # learn a new programming language or technology.
    # Each coding challenge is based on real world tools and utilities.
    # Typical projects have included: wc, cat, uniq, Redis, NATS, memcached, grep,
    # git, web server, irc client, head, jq, and a password cracker."""
    
    print("\nInitializing chatbot...")
    try:
        chatbot = AIChatbot(api_key=api_key, system_prompt=system_prompt)
        print("Chatbot ready! Type 'quit', 'exit', or 'bye' to end the conversation.")
        print("Type 'clear' to clear conversation history.")
        print("=" * 60)
        print()
        
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        sys.exit(1)
    
    # Main chat loop
    while True:
        try:
            # Get user input
            user_input = input("Your query: ").strip()
            
            if not user_input:
                continue
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\nGoodbye! Happy coding! 👋")
                break
            
            # Check for clear command
            if user_input.lower() == 'clear':
                chatbot.clear_history()
                print("\n[Conversation history cleared]\n")
                continue
            
            # Send message and get streaming response
            chatbot.send_message(user_input, stream=True)
            print()  # Extra line for readability
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Happy coding! 👋")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
