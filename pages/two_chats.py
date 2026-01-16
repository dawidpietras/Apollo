import streamlit as st
import asyncio
from backend.llm_client import get_async_client

client = get_async_client()



async def stream_to_placeholder(prompt, placeholder):
    stream = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Jesteś filozofem i na zadanie pytanie odpowiadasz z dwóch przeciwstawnych stron."},
            {"role": "user", "content": prompt}],
        model="gpt-5.2",
        stream=True,
        max_completion_tokens=300
    )

    response = ""
    async for chunk in stream:
        chunk_content = chunk.choices[0].delta.content
        if chunk_content:
            response += chunk_content

        placeholder.markdown(response)
            
async def run_parallel_queries():
    col1, col2 = st.columns(2)
    placeholder1 = col1.empty()
    placeholder2 = col2.empty()
    
    await asyncio.gather(
        stream_to_placeholder("Sens życia", placeholder1),
        stream_to_placeholder("Gromadzenie bogactw i praca", placeholder2)
    )


st.title("Async is King!")

if st.button("Zadaj pytania"):
    # Ponieważ Streamlit jest synchroniczny, musimy "odpalić" pętlę asyncio
    asyncio.run(run_parallel_queries())