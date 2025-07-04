from PIL import Image
import numpy as np
import streamlit as st
from tensorflow.keras.saving import load_model
from tensorflow.keras.preprocessing import image

labels = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z', 'nothing', 'space', 'del']



def preprocess_PIL(pil_img, input_size=(128, 128)):
    pil_img = pil_img.convert("RGB")
    img = pil_img.resize(input_size)
    img_array = image.img_to_array(img)

    img_array = np.expand_dims(img_array, axis=0) #Thêm n = 1 để batch_size = 1
    test_datagen = image.ImageDataGenerator(                           # Bắt buộc áp các phương pháp tiền xử lý như tập train
        samplewise_center=True,            
        samplewise_std_normalization=True
    )
    img_generator = test_datagen.flow(img_array, batch_size=1)
    return img_generator


def main():
    @st.cache_resource
    def load_asl_model(model_path='model.keras'):
        try:
            model = load_model(model_path)
            return model
        except Exception as e:
            st.error(f"Error loading model")
            return None
    
    model = load_asl_model("model_epoch_04.keras")


    st.title("American ASL Classifiaction App")

    option = st.selectbox("Choose input type", ("Upload Image","Use Webcam"))

    if option == "Upload Image":
        uloaded_file = st.file_uploader("Choose an image ...", type=["jpg","jpeg","png"])
        if uloaded_file is not None:
            image = Image.open(uloaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            if st.button("Classify"):
                img_gen = preprocess_PIL(image)
                predictions = model.predict(next(img_gen))
                prediction_idx = np.argmax(predictions)
                predicted_label = labels[prediction_idx]
                confidence = np.max(predictions)
                st.write(f"**Prediction:** {predicted_label} with {confidence*100:.2f}% confidence.")
    
    elif option == "Use Webcam":
        st.write("Realtime ASL detected using Webcam")



if __name__ == "__main__":
    main()






