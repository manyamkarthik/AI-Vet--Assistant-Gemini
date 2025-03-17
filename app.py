import os
import streamlit as st
import google.generativeai as genai
from PIL import Image


def chat_func(prompt, img):
    model = genai.GenerativeModel('gemini-1.5-flash')

    try:
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"An error occurred: {e}. Please try again."

def convert_image_to_pil(st_image):
    import io
    image_data = st_image.read()
    pil_image = Image.open(io.BytesIO(image_data))
    return pil_image

if __name__ == "__main__":
    
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)

    st.image('banner.png') # Replace with a vet-themed banner if you have one
    st.title('Veterinary AI Assistant')

    # Mobile-friendly layout: put elements in a single column by default
    col1, = st.columns(1)  # Create one column for now

    with col1:  # Put elements inside this column
        img = st.file_uploader("Upload an animal image", type=['png', 'jpg', 'jpeg','gif'])

        if img:
            st.image(img, caption='Image of the animal')

            # Enhanced Veterinary Prompt
            prompt = st.text_area('Describe the symptoms or ask a question about the animal\'s condition:')

            # Analyze Button
            if st.button("Analyze"):  # Separate button
                if prompt:
                    pil_image = convert_image_to_pil(img)

                    # Modified Prompt
                    veterinary_prompt = f"""
        **Prompt:**

You are a veterinary AI assistant designed to analyze images of animals and provided symptom descriptions or questions from veterinarians. Your response should include the following structured elements:

1. **Image Analysis**: Describe your observations based on the image of the animal, identifying visible symptoms or conditions.

2. **Possible Diagnoses**: Based on the image analysis and symptom description, list potential diagnoses. Include common diseases that affect animals in India, considering factors like species, age, and environment.

3. **Treatment Recommendations**:
   - Suggest potential treatments including:
     - **Medications**: Specify names, dosages, and any relevant administration methods (oral, injectable, topical, etc.)
     - **Non-Medication Treatments**: Include any necessary changes in diet, exercise, or lifestyle.
   - Mention any potential drug interactions or contraindications relevant to the suggested treatments.

4. **Language Requirement**: Provide your entire response in both Telugu and English. The Telugu response should come first, followed by the English translation.

5. **Disclaimer**: Clearly state that your suggestions are for informational purposes only and must be validated by a qualified veterinarian before implementation.

6. **Contextual Sensitivity**: Ensure that your recommendations consider the veterinary practices and common animal health issues prevalent in India.

**Example Response Structure**:

**Telugu:**
1. పిక్చర్ విశ్లేషణ: ...
2. సంభావ్య వ్యాధులు: ...
3. చికిత్సా సిఫార్సులు:
   - మందులు: ...
   - మార్గదర్శకాలు: ...
4. నోటీసు: ...

**English:**
1. Image Analysis: ...
2. Possible Diagnoses: ...
3. Treatment Recommendations:
   - Medications: ...
   - Non-Medication Treatments: ...
4. Disclaimer: ...
                    """

                    with st.spinner('Analyzing the image and generating recommendations...'):
                        answer = chat_func(veterinary_prompt, pil_image)
                        st.text_area('Gemini Answer:', value=answer, height=300)


                    if 'history' not in st.session_state:
                        st.session_state.history = 'Chat History\n'

                    value = f'**Question**: {prompt}: \n\n **Answer**: {answer}'
                    st.session_state.history = f'{value} \n\n {"-" * 100} \n\n {st.session_state.history}'

                    h = st.session_state.history
                    st.text_area(label='Chat History:', value=h, height=800, key='history')
