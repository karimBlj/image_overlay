import pandas as pd
from datetime import datetime
from smtp_test import is_valid_email
from img_loader import ImgLoader
from email_handler import EmailHandler
from utils import (
    upload_image,
    read_json_file,
    load_email_content,
    load_history_campaigns
)

config = read_json_file("config.json")

df_leads  = pd.read_csv(config["path_leads_file"], sep="\t")
df_result = pd.DataFrame(
    columns = [
        "date",
        "name",
        "domain",
        "location",
        "email",
        "img_inserted_path",
        "img_inserted_url",
        "zoho_api_response",
        "message_id"
    ]
)

path_base_img = config["path_base_img"]
folder_img_generated = config["folder_img_generated"]
imgLoader = ImgLoader(path_base_img, folder_img_generated)
imgLoader.init_points()
imgLoader.adjust_points()

handler = EmailHandler()
handler.generate_token()

history = load_history_campaigns()

try:
    for i in range(len(df_leads)):
        row = df_leads.iloc[i]
        print(row)
        email =  row["Email"]
        if not is_valid_email(email):
            print(f"email {email} is considered invalid")
            continue
        # email =  "rimukus@gmail.com"
        if email in df_result["email"].values or email in history["email"].values:
            continue

        image_inserted_path = imgLoader.create_overlayed_image_from_website("https://" + row["Domain"], row["Company name"] + ".png")
        
        print("######## WESH #########")
        print(image_inserted_path)
        img_url = upload_image(image_inserted_path, "zoho_campaign/" + row["Company name"] + ".png")
        # img_url = upload_image(image_inserted_path, "zoho_campaign/" + "kb_bk" + ".png")


        print(img_url)
        content = load_email_content(config["path_email_template"], img_url, row["Company name"], row["IndustryMail"])
        email_data = handler.send_email(
            email,
            "Curious About " + row["Company name"] + " Data Potential?",
            content
        )

        print(email_data)
        print(email_data["data"]["messageId"])
        record = {
            "date"              : [datetime.now()                 ],
            "name"              : [row["Company name"]            ],
            "domain"            : [row["Domain"]                  ],
            "location"          : [row["Location"]                ],
            "email"             : [email                          ],
            "img_inserted_path" : [image_inserted_path            ],
            "img_inserted_url"  : [img_url                        ],
            "zoho_api_response" : [email_data                     ],
            "message_id"        : [email_data["data"]["messageId"]],
        }

        df_result = pd.concat([df_result, pd.DataFrame(record)])
    
except Exception as e:
    df_result.to_csv(config["path_result_report"] + "report.csv")
    raise e

df_result.to_csv(config["path_result_report"] + "report.csv", index = False, sep = "|")


#TODO:
# Update subject
# change email
# cahnge for loop length
# un comment update email