import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from data.multimodal import image_ocr, pdf_reader
from blackhole_core.agents.archive_search_agent import ArchiveSearchAgent
from blackhole_core.data_source.mongodb import get_agent_outputs_collection

def run_pipeline():
    print("🚀 Starting Combined Demo Pipeline...\n")

    # Process Image
    image_path = r"data/multimodal/black-white-color-quotes-dave-matthews-nothing-is-black-or-white-nothings-us-o-2042.webp"
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return

    extracted_text_img = image_ocr.extract_text_from_image(image_path, debug=True)
    print("\n🖼️ Extracted Text from Image:\n", extracted_text_img)

    # Process PDF
    pdf_path = r"data/multimodal/mathbook.pdf"
    extracted_text_pdf = pdf_reader.extract_text_from_pdf(pdf_path, include_page_numbers=True, verbose=True)
    print("\n📄 Extracted Text from PDF:\n", extracted_text_pdf)

    # If there was an error with the PDF, handle it
    if extracted_text_pdf.startswith("❌"):
        print(f"Error processing PDF: {extracted_text_pdf}")
        return

    # Combine both texts
    combined_text = extracted_text_img + "\n\n" + extracted_text_pdf

    # Pass to ArchiveSearchAgent
    agent = ArchiveSearchAgent()
    result = agent.plan({"document_text": combined_text})
    print("\n📊 Agent Output:\n", result)

    # Save result to MongoDB
    result.pop("_id", None)
    try:
        collection = get_agent_outputs_collection()
        collection.insert_one(result)
        print("\n✅ Agent output saved to MongoDB.")
    except Exception as e:
        print(f"\n❌ Error saving to MongoDB: {e}")

if __name__ == "__main__":
    run_pipeline()
