import streamlit as st 
import google.generativeai as genai

#------------------------------------------
# CONFIGURATION
#------------------------------------------
st.set_page_config(page_title="Gemini RAG App", page_icon=":robot_face:", layout="centered")
st.title("Prompt engineering using Gemini")

# Gemini API key input (for demo purposes, you can set this as an environment variable in production
api_key = st.text_input("Enter your Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # Dummy retriever for demonstration
    def retrieved_info(query):
        # Here you could add a vector search, database lookup, or PDF retriever
        return "Explain about indias economy"
    
    # MAIN RAG FUNCTION
    def rag_query(query):
        retrieved = retrieved_info(query)   # ✅ different name

        augmented_prompt = f"""
          User query: {query}
          Retrieved info: {retrieved}
           Answer the question based on the retrieved info.
            """
        model_name = "models/gemini-3-flash-preview"
        model = genai.GenerativeModel(model_name)
        
        response = model.generate_content(
            augmented_prompt,
            generation_config={
                "temperature": 1.0,
                "max_output_tokens": 1000,
                "top_p": 1.0,
                "top_k": 55,
                "stop_sequences": ["End"],
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
            }
        )
        return response.text.strip()
    
    #----------------------------------
    # UI Section
    #----------------------------------
    query = st.text_area("I am bot:", "How may i help you")
    
    if st.button("Generate Response"):
        if not query.strip():
            st.warning("Please enter a query.")
        else:
            with st.spinner("Generating response..."):
                try:
                    answer = rag_query(query)
                    st.success("Response Generated!")
                    st.markdown(f"**Answer:**\n\n{answer}")
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.info("Please enter your Gemini API Key to start.")
    
#------------------------------------------
# Footer
#------------------------------------------
st.markdown("---")
st.caption("Built with Streamlit and Gemini API + Azad")
                                          