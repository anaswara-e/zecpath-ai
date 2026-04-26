from parsers.jd_parser import parse_jd
import os
import json


def test_multiple_jds():

    folder_path = "data/job_descriptions"
    output_folder = "data/structured_jd"

    # create output folder if not exists
    os.makedirs(output_folder, exist_ok=True)

    results = []

    for file in os.listdir(folder_path):

        if file.endswith(".txt"):
            file_path = os.path.join(folder_path, file)

            with open(file_path, "r", encoding="utf-8") as f:
                jd_text = f.read()

            result = parse_jd(jd_text)

            # optional: store file name also
            result["file_name"] = file

            results.append(result)

    # save all outputs
    output_file = os.path.join(output_folder, "all_jds.json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print("Total JDs processed:", len(results))

    assert len(results) > 0