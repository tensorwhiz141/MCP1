# # import sys
# # import os

# # # Add project root to sys.path
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# # from data.multimodal import image_ocr
# # from blackhole_core.agents.archive_search_agent import ArchiveSearchAgent
# # from blackhole_core.data_source.mongodb import get_agent_outputs_collection

# # def process_image_with_agent(image_path):
# #     print(f"\n🖼️  Processing Image: {image_path}")

# #     extracted_text = image_ocr.extract_text_from_image(image_path, debug=True)
# #     print("\n🔍 Extracted Text Preview:\n", extracted_text)

# #     agent = ArchiveSearchAgent()
# #     agent_output = agent.plan({"document_text": extracted_text})
# #     print("\n📊 Agent Output:\n", agent_output)

# #     result_record = agent_output
# #     result_record.pop("_id", None)

# #     try:
# #         collection = get_agent_outputs_collection()
# #         collection.insert_one(result_record)
# #         print("✅ Agent output saved to MongoDB.")
# #     except Exception as e:
# #         print(f"❌ Error saving to MongoDB: {e}")

# # if __name__ == "__main__":
# #     image_path = r"data\multimodal\black-white-color-quotes-dave-matthews-nothing-is-black-or-white-nothings-us-o-2042.webp"

# #     if not os.path.exists(image_path):
# #         print(f"❌ Image file not found: {image_path}")
# #     else:
# #         process_image_with_agent(image_path)


# import os
# from data.multimodal import pdf_reader, image_ocr
# from blackhole_core.agents.archive_search_agent import ArchiveSearchAgent

# def run_pipeline():
#     print("=== Starting Blackhole Demo Pipeline ===")

#     pdf_path = os.path.join("data", "multimodal", "sample.pdf")
#     image_path = os.path.join("data", "multimodal", "qNVTp_preprocessed.png")

#     pdf_text = pdf_reader.extract_text_from_pdf(pdf_path)
#     print(f"\nExtracted text from PDF:\n{pdf_text}")

#     image_text = image_ocr.extract_text_from_image(image_path)
#     print(f"\nExtracted text from Image:\n{image_text}")

#     agent = ArchiveSearchAgent()

#     combined_input = pdf_text + "\n" + image_text
#     result = agent.search_archive(combined_input)

#     print("\nFinal Insight from ArchiveSearchAgent:")
#     print(result)

# if __name__ == "__main__":
#     run_pipeline()


import sys
import os
import traceback

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from data.multimodal import image_ocr
from blackhole_core.agents.archive_search_agent import ArchiveSearchAgent
from blackhole_core.data_source.mongodb import get_agent_outputs_collection

def process_image_with_agent(image_path):
    print(f"\n🖼️  Processing Image: {image_path}")

    try:
        # Extract text
        extracted_text = image_ocr.extract_text_from_image(image_path, debug=True)
        print("\n🔍 Extracted Text Preview:\n", extracted_text)

        # Initialize agent and search
        try:
            agent = ArchiveSearchAgent()
            agent_output = agent.plan({"document_text": extracted_text})
            print("\n📊 Agent Output:\n", agent_output)

            # Remove _id before saving
            result_record = agent_output
            if isinstance(result_record, dict):
                result_record.pop("_id", None)

                # Save result to MongoDB
                try:
                    collection = get_agent_outputs_collection()
                    collection.insert_one(result_record)
                    print("✅ Agent output saved to MongoDB.")
                except Exception as e:
                    print(f"❌ Error saving to MongoDB: {e}")
                    print("⚠️ Continuing without saving to database...")
            else:
                print("❌ Agent output is not a dictionary, cannot save to MongoDB.")

        except Exception as agent_error:
            print(f"❌ Error with ArchiveSearchAgent: {agent_error}")
            traceback.print_exc()

    except Exception as e:
        print(f"❌ Error processing image: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    try:
        # Use os.path.join for cross-platform compatibility
        image_path = os.path.join("data", "multimodal", "black-white-color-quotes-dave-matthews-nothing-is-black-or-white-nothings-us-o-2042.webp")

        if not os.path.exists(image_path):
            print(f"❌ Image file not found: {image_path}")
            # Try alternative path format
            image_path = r"data\multimodal\black-white-color-quotes-dave-matthews-nothing-is-black-or-white-nothings-us-o-2042.webp"
            if not os.path.exists(image_path):
                print(f"❌ Alternative image path also not found: {image_path}")
            else:
                process_image_with_agent(image_path)
        else:
            process_image_with_agent(image_path)
    except Exception as e:
        print(f"❌ Unhandled error: {e}")
        traceback.print_exc()
