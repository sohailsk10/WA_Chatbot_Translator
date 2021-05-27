import speech_recognition as sr
from watson_developer_cloud import AssistantV1, LanguageTranslatorV3
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pyttsx3
from gtts import gTTS
from playsound import playsound
import os

from ibm_watson import AssistantV2
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


from gtts import gTTS
# consts
BASE_LANGUAGE = 'en'
LT_THRESH = 0.4
LT_PAIRS = {
    'ar': 'Arabic',
    'bg': 'Bulgarian',
    'zh': 'Chinese (Simplified)',
    'zht': 'Chinese (Traditional)',
    'hr': 'Croatian',
    'cz': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'et': 'Estonian',
    'el': 'Greek',
    'en': 'English',
    'fi': 'Finnish',
    'fr': 'French',
    'de': 'German',
    'hi': 'Hindi',
    'he': 'Hebrew',
    'id': 'Indonesian',
    'lt': 'Lithuanian',
    'lv': 'Latvian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ms': 'Malay',
    'nb': 'Norwegian Bokmal',
    'pl': 'Polish',
    'pt': 'Portuguese (Brazil)',
    'ru': 'Russian',
    'ro': 'Romanian',
    'es': 'Spanish',
    'sl': 'Slovenian',
    'sk': 'Slovak',
    'sv': 'Swedish',
    'th': 'Thai',
    'er': 'Urdu',
    'vi': 'Vietnamese',
    'tr': 'Turkish'
}

workspace_id = "117d6a47-0c7a-4751-be87-4996ffb1aeeb"
# assistant_api_key = "Dd0NrWCuy1222pjjGPJ97bPer-NytxAgxOZpXc1EV0xN"
assistant_api_key = "Gkad4F_myreduRm6a0B_pImofiXS9lptw4B1lp2Z5gPn"
# translator_api_key = "ut5yA-d4A73QZGth02NUwB7nyYwFDq8hupd8pZXrU1ET"
translator_api_key = "pb9SUMxSl7OcpjXwJty8FxH_fxM51Kd7T7gU8nFtRdnH"

r = sr.Recognizer()

lang = "es"

def main():

    # get conversation workspace id
    try:
        workspace = workspace_id
    except:
        return {
            'message': 'Please bind your assistant workspace ID as parameter',
            'context': '{}',
            'output': '{}',
            'intents': '{}',
            'language': ''
        }

    # set up conversation
    try:
        # assistant = AssistantV1(iam_apikey=assistant_api_key, version='2019-03-06')
        authenticator = IAMAuthenticator(assistant_api_key)
        assistant = AssistantV2(
            version='2020-04-01',
            authenticator=authenticator
        )
        assistant.set_service_url('https://api.eu-gb.assistant.watson.cloud.ibm.com/instances/76fa3d44-f247-4a0b-a826-ff47eb98a891')

    except:
        return {
            'message': 'Please bind your assistant service',
            'context': '{}',
            'output': '{}',
            'intents': '{}',
            'language': ''
        }

    try:
        # translator = LanguageTranslatorV3(version='2019-04-03', iam_apikey=translator_api_key)
        # translator = LanguageTranslatorV3(iam_apikey = translator_api_key)
        authenticator = IAMAuthenticator(translator_api_key)
        translator = LanguageTranslatorV3(
            version='2018-05-01',
            authenticator=authenticator
        )
        print(translator)
        translator.set_service_url('https://api.us-south.language-translator.watson.cloud.ibm.com/instances/5e8a8531-a1d8-493d-86db-a27a82d1ffbf')
    except:
        return {
            'message': 'Please bind your language translator service',
            'context': '{}',
            'output': '{}',
            'intents': '{}',
            'language': ''
        }

    context = {}

    Session_ID = assistant.create_session(
        assistant_id='64e050a6-6669-412c-8fca-fd4698c4ddb0'
    )
    sess_id = Session_ID.get_result()['session_id']

    while True:
        # try:
        #     text = input("Input Text: ")
        # except:
        #     text = ''

        try:
            # use the microphone as source for input.
            # with sr.Microphone() as source:
            #     engine = pyttsx3.init()
            # #     # engine.say(text)
            #     engine.runAndWait()
            #     print('Say Something')
            #     audio = r.listen(source)
            #     print(audio)
            #     r.adjust_for_ambient_noise(source, duration=0.05)
            #     said = r.recognize_google(audio, language="ar")
            #     print(said)
            #     # temp = r.recognize_google(audio)
            #     # print("temp", temp)
            # #
            #     if (lang == 'en') :
            #         said = r.recognize_google(audio, language='en-US')
            #         print("Said_en", said)
            #     elif (lang == 'es') :
            #         said = r.recognize_google(audio, language="ar")
            #         print("Said_es", said)

                # print("Start recordng")

                #
                # audio2 = r.listen(source)
                # print('audio2', audio2)

                # Using ggogle to recognize audio
                # Mytext = r.recognize_google(audio)
                # print("MyText", Mytext)
                text = input("type something: ")

                # text = text.lower()
                # print("Did you say " + Mytext)
                # text = Mytext



        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occured")

        # get conversation context if available
        # try:
        #     # print("Context")
        #     context = json.loads( params['context'] )
        #     print('context: ', context)
        # except:

        # if context != None:
        #     pass

        # detect language
        if text:
            response = translator.identify(text)
            res = response.get_result()
        else:
            res = None

        if res and res['languages'][0]['confidence'] > LT_THRESH:
            language = res['languages'][0]['language']
        elif res is None:
            language = BASE_LANGUAGE
        else:
            print('message Sorry, I am not able to detect the language you are speaking. Please try rephrasing.'),
            context = context
            continue
        #     output = '{}',
        #     intents = '{}',
        # language = ''

        if language not in LT_PAIRS.keys():
            print('message: Sorry, I do not know how to translate between {} and {} yet.'.format(BASE_LANGUAGE, language))
            context = context
            continue
            # output = '{}'
            # intents = '{}'
            # language = language

        # translate to base language if needed
        # try:
        if language != BASE_LANGUAGE:
            response = translator.translate(
                text,
                source=language,
                target=BASE_LANGUAGE
            )
            res = response.get_result()
            text = res['translations'][0]['translation']
            print("TEXT", text)

        # supply language as entity
        text += ' (@language:{})'.format( language )

        # hit conversation
        # response = assistant.message(
        #     workspace_id=workspace,
        #     input={'text': text},
        #     context=context
        # )

        response = assistant.message(
            assistant_id='64e050a6-6669-412c-8fca-fd4698c4ddb0',
            session_id=sess_id,
            input={'text': text},
            context=context
            # input={
            #     'message_type': 'text',
            #     'text': 'Hello'
            # }
        )

        res = response
        new_res = res.get_result()
        def_context = new_res
        print("NEW_RES", new_res)
        new_context = new_res['output']['generic'][0]['text']
        print("new_context", new_context)

        output = new_context
        print("OUTPUT", output)
        # output_text = [text for text in new_context if text]
        output_text = output
        Output_TEXT = output_text


        message = Output_TEXT
        # print("MESSAGE", message)
        # output['text'] = output_text
        # # intents = res['intents']
        # print(intents)

        # translate back to original language if needed
        if language != BASE_LANGUAGE:
            response = translator.translate(
                Output_TEXT,
                source=BASE_LANGUAGE,
                target=language
            )
            res = response.get_result()
            Output_TEXT = [t['translation'] for t in res['translations']]
            print("Output_TEXT", Output_TEXT)
            message = Output_TEXT
            # output['text'] = Output_TEXT
        print("Reply: ", message)
        message = "".join(message)
        tts = gTTS(text=message, lang=language)
        tts.save("detect.mp3")
        playsound('detect.mp3')
        os.remove('detect.mp3')
        print("LANGUAGE DETECTED: ", language)

        # print(type(new_context))
        # print(new_context)
        context = def_context
        # else:
        # message = message

main()


