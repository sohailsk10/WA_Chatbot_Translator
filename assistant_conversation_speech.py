import speech_recognition as sr
from watson_developer_cloud import AssistantV1, LanguageTranslatorV3
import pyttsx3
from gtts import gTTS
from playsound import playsound
import os


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

workspace_id = "473014ec-a7a6-4ef0-a994-6d89330dba41"
assistant_api_key = "Dd0NrWCuy1222pjjGPJ97bPer-NytxAgxOZpXc1EV0xN"
translator_api_key = "ut5yA-d4A73QZGth02NUwB7nyYwFDq8hupd8pZXrU1ET"

r = sr.Recognizer()
lang = "es"

def main():

    # get conversation workspace id
    try:
        workspace = workspace_id
    except Exception as ex:
        print(ex)
        return {
            'message': 'Please bind your assistant workspace ID as parameter',
            'context': '{}',
            'output': '{}',
            'intents': '{}',
            'language': ''
        }

    try:
        assistant = AssistantV1(
            iam_apikey=assistant_api_key,
            version='2019-03-06'
        )
    except:
        return {
            'message': 'Please bind your assistant service',
            'context': '{}',
            'output': '{}',
            'intents': '{}',
            'language': ''
        }

    try:
        translator = LanguageTranslatorV3(
            version='2019-04-03',
            iam_apikey=translator_api_key
        )
    except:
        return {
            'message': 'Please bind your language translator service',
            'context': '{}',
            'output': '{}',
            'intents': '{}',
            'language': ''
        }

    context = {}
    while True:
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source:
                print('Say Something')
                # audio = r.listen(source)
                # print(audio)
                r.adjust_for_ambient_noise(source, duration=0.05)
                print("Recording for 4 seconds")
                recorded_audio = r.listen(source, timeout=4)
                said = r.recognize_google(recorded_audio, language="hi-IN")
                print(said)
                # break
                # temp = r.recognize_google(audio)
                # print("te mp", temp)
            #
                # if (lang == 'en') :
                #     said = r.recognize_google(audio, language='en-US')
                #     print("Said_en", said)
                # elif (lang == 'ar') :
                #     said = r.recognize_google(audio, language="ar")
                #     print("Said_es", said)

                print("Start recordng")

                #
                # audio2 = r.listen(source)
                # print('audio2', audio2)

                # Using ggogle to recognize audio
                # Mytext = r.recognize_google(audio)
                # print("MyText", Mytext)
                # text = input("type something: ")

                # text = text.lower()
                print("Did you say " + said)
                text = said



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
            language = language

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

        # supply language as entity
        text += ' (@language:{})'.format( language )

        # hit conversation
        response = assistant.message(
            workspace_id=workspace,
            input={'text': text},
            context=context
        )

        res = response.get_result()
        new_res = response.get_result()
        new_context = res['context']
        output = res['output']
        output_text = [text for text in res['output']['text'] if text]
        message = output_text[0]
        output['text'] = output_text
        intents = res['intents']
        # print(intents)

        # translate back to original language if needed
        if language != BASE_LANGUAGE:
            response = translator.translate(
                output_text,
                source=BASE_LANGUAGE,
                target=language
            )
            res = response.get_result()
            output_text = [t['translation'] for t in res['translations']]
            message = output_text[0]
            output['text'] = output_text
        print("Reply: ", message)

        tts = gTTS(text=message, lang=language)
        tts.save("test.mp3")
        playsound('test.mp3')
        os.remove('test.mp3')
        print("LANGUAGE DETECTED: ", language)

        context = new_res['context']
main()
