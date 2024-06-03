import google.generativeai as genai
import smtplib 
from email.message import EmailMessage
from html import generate_html
from dotenv import load_dotenv
import os

load_dotenv()
EMAILS = os.getenv('EMAILS').split(",")

def ask_to_gemini(isDefTrigerrefFromOutside=False):

   genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
   model = genai.GenerativeModel('gemini-1.0-pro-latest')
   response = model.generate_content(f"ingilizce öğrenme sürecinde olan birine bir adet ingilizce kelime,kelimenin 3 adet cümle içinde kullanımı,kelimenin etomolijik kökenini ve bu cümlelerin türkçelerini de yazmalısın. seçeceğin ingilizce kelime çok zor olmamalı a2/b1 seviyelerinde bir kelime seçmen daha yararlı olur. Kelime günlük kullanımda da sık yer alıyorsa daha da iyi olur. Cevabı sırası ile Kelime , Kelimenin Anlamı, Etimolojik Köken , İngilizce Cümleler(burada ingilizce cümlenin türkçesi de olmalı her cümle için) olarak göndermelisin.")
   emails=EMAILS
   #dev_mail=["mert.915@hotmail.com"]

   new_response = response.text.replace("\n\n","\n")
   new_response_arry = new_response.split("\n")
   new_response_arry = [text.replace("**", "") for text in new_response_arry]
   new_response_arry = [text.replace("*", "") for text in new_response_arry]
   if isDefTrigerrefFromOutside == True:
      print(new_response_arry)
      return new_response_arry
   
   mail_adres = os.getenv('MAIL_ADRES')
   mail_password = os.getenv('MAIL_PASSWORD')
   mail = EmailMessage()
   mail['Subject'] = f"Günaydın günün ingilizce kelimesi hazır"
   mail['From'] = "Daily English Word Bot <ozlemk.1667@gmail.com>"
   mail['To'] = emails
   print(new_response_arry)
   res_html = generate_html(new_response_arry)
   mail.add_alternative(res_html, subtype='html')

   if __name__ == "__main__":
      with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
         smtp.login(mail_adres, mail_password)
         smtp.send_message(mail)
         print("mail gönderildi")

ask_to_gemini()

