import pathlib
from pytube import YouTube 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
import os 
import re
import random

def set_ffmpeg_paths(ffmpeg_path):
    AudioSegment.ffmpeg = ffmpeg_path
    AudioSegment.converter = ffmpeg_path

def download_video_as_audio(video_url, export_path):
    print("Подготовка к скачиванию...")
    yt = YouTube(video_url) 
    video = yt.streams.filter(only_audio=True).first() 
    print("Скачивание...")
    outfile = video.download(output_path=export_path) 
    base, ext = os.path.splitext(outfile) 
    new_file = str(export_path) + "\\downloaded_audio.mp3"
    os.replace(outfile, new_file)
    print("Аудио успешно скачано!")
    return new_file

def convert_to_wav(audio_file):
    print("Приеобразование в WAV...")
    sound = AudioSegment.from_file(audio_file, format="mp4")
    new_file = audio_file[:-3] + "wav"
    sound.export(new_file, format="wav")
    print("Аудио успешно преобразовано в WAV!")
    return new_file

def split_audio(audio_file, split_audio_path):
    print("Подготовка к разделению...")
    sound = AudioSegment.from_file(audio_file, format="wav") 
    audiochunks = split_on_silence(sound,min_silence_len=89,silence_thresh=-29)
    for i, chunk in enumerate(audiochunks):
        outputfile = AudioSegment.silent(duration=1000) + chunk + AudioSegment.silent(duration=1000)
        outputfile.export(split_audio_path + "\\word{0}.wav".format(i), format="wav")
        print('Сохранение файла под номером ' + str(i))

def recognize_audio(split_audio_path, renamed_audio_path, language_code = 'ru'):
    itera = input("Введите код итерации: ")
    print("Подготовка к распознованию...")
    for filename in os.listdir(split_audio_path):
        ofset = int(filename.replace('word','').replace('.wav',''))
        r = sr.Recognizer()
        with sr.AudioFile(split_audio_path + '\\{0}'.format(filename)) as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                speech = r.recognize_whisper(audio, model="base", language=language_code).lower()
            except sr.UnknownValueError:
                speech = "UVE"
            if "редактор субтитров а.семкин корректор а.егорова" in speech:
                speech = "UVE"
            if speech != "UVE":
                print('Распознано: ' + speech)
            else:
                print('Файл ' + filename + ' не был распознан')
        if len(speech) <= 100:
            os.rename(split_audio_path + "\\word{0}.wav".format(ofset), renamed_audio_path + "\\" + re.sub(r'\W+', ' ', speech) + "(" + str(ofset) + ")(" + itera + ")" + ".wav")
        else:
            os.remove(split_audio_path + "\\word{0}.wav".format(ofset))

def trim_audio(renamed_audio_path, ready_audio_path):
    print("Подготовка к обрезке...")
    for filename in os.listdir(renamed_audio_path):
        if "UVE" in filename:
            print('Файл ' + filename + ' не был разпознан')
        else:
            print("Обрезка файла " + filename)
            sound = AudioSegment.from_file(renamed_audio_path + "\\" + filename, format="wav")
            ready = sound[1000:-1000]
            ready.export(ready_audio_path + '\\' + filename,format="wav")
        os.remove(renamed_audio_path + "\\" + filename)
        print("Удаление файла " + filename)


def my_shuffle(lst):
    shuf_lst = lst.copy()
    random.shuffle(shuf_lst)
    return shuf_lst

def fly_ascii_face_gen():
    #(" ║" + my_shuffle([" ╭──", " ╭^^", " ╭┴─"," /‾‾", " ╭┬┬"])[0] + my_shuffle(["─", "^", "‾","┴", "v", "┼"])[0] + my_shuffle(["──╮ ", "^^╮ ", "─┴╮ ","‾‾\ ", "┬┬╮ "])[0] + "║\n")
    #(" ║" + my_shuffle([" (o ", " () ", " (O ", " (o)", " ( )", " (.)", " (<>", " (Oo"])[0] + my_shuffle([" ", " ", " ", "^", "v"])[0] + my_shuffle([" o) ", " () ", " O) ", "(o) ", "( ) ", "(.) ", "<>) ", "oO) "])[0] + "║\n")
    #(" ║" + my_shuffle([" \ /", " \  ", " \┼ ", " ╰ _", " ╰╮ "])[0] + my_shuffle([" ", " ", "|", "v", "^", "┼"])[0] + my_shuffle(["\ / ", "  / ", " ┼/ ", "_ ╯ ", " ╭╯ "])[0] + "║\n")
    #(" ║" + my_shuffle(["  ╰┴", "  ╰┬", "  \_", "  ╰v","  ╰─", "  /|", "  ╰┼", "  \/"])[0] + my_shuffle(["─","┴", "_", "v", "┼", "┬"])[0] + my_shuffle(["┴╯  ", "┬╯  ", "_/  ", "v╯  ","─╯  ", "|\  ", "┼╯  ", "\/  "])[0] + "║\n")

    ascii_art = ""
    ascii_art += my_shuffle([" ╔═════════╗\n"," ╔═════════╗\n"," ╔═════════╗\n", " ╔═════════╗\n", " ╔═════════╗\n", " ╔═════════╗\n", " ╔═════════╗\n", " ╔═════════╗\n", " ╔═════════╗\n", " ╔═════════╗\n", " ╔═════════╗\n", " ╔═════════╗\n", " ╔═══╡*╞═══╗\n"])[0]
    ascii_art += my_shuffle([" ║ ╭─────╮ ║\n"," ║ ╭^^^^^╮ ║\n"," ║ ╭(‾‾‾)╮ ║\n", " ║ ╭┴───┴╮ ║\n", " ║ ╭~~─~~╮ ║\n", " ║ /‾‾‾‾‾\ ║\n", " ║ ╭┬─┴─┬╮ ║\n", " ║ ._._._. ║\n", " ║ _/‾‾‾\_ ║\n", " ║ ╭┬┬┬┬┬╮ ║\n", " ║ ╭┴─┼─┴╮ ║\n", " ║ /‾‾v‾‾\ ║\n", (" ║" + my_shuffle([" ╭──", " ╭^^", " ╭┴─"," /‾‾", " ╭┬┬"])[0] + my_shuffle(["─", "^", "‾","┴", "v", "┼"])[0] + my_shuffle(["──╮ ", "^^╮ ", "─┴╮ ","‾‾\ ", "┬┬╮ "])[0] + "║\n")])[0]
    ascii_art += my_shuffle([" ║ (o   o) ║\n"," ║ O  ^  O ║\n"," ║ .)   (. ║\n", " ║ ()   () ║\n", " ║ (o) (o) ║\n", " ║ (O   O) ║\n", " ║ ( ) ( ) ║\n", " ║ (.) (.) ║\n", " ║ (-) (-) ║\n", " ║ (<> <>) ║\n", " ║ (Oo oO) ║\n", " ║ (Θ)|(Θ) ║\n", (" ║" + my_shuffle([" (o ", " () ", " (O ", " (o)", " ( )", " (.)", " (<>", " (Oo"])[0] + my_shuffle([" ", " ", " ", "^", "v"])[0] + my_shuffle([" o) ", " () ", " O) ", "(o) ", "( ) ", "(.) ", "<>) ", "oO) "])[0] + "║\n")])[0]
    ascii_art += my_shuffle([" ║ \ / \ / ║\n"," ║ \ ╭┼╮ / ║\n"," ║ ╰╮   ╭╯ ║\n", " ║ | / \ | ║\n", " ║ ╰ _ _ ╯ ║\n", " ║ \  |  / ║\n", " ║ \  ^  / ║\n", " ║ \  v  / ║\n", " ║ ‾\   /‾ ║\n", " ║ \ ┬ ┬ / ║\n", " ║ \┼   ┼/ ║\n", " ║ \ ┬ ┬ / ║\n", (" ║" + my_shuffle([" \ /", " \  ", " \┼ ", " ╰ _", " ╰╮ "])[0] + my_shuffle([" ", " ", "|", "v", "^", "┼"])[0] + my_shuffle(["\ / ", "  / ", " ┼/ ", "_ ╯ ", " ╭╯ "])[0] + "║\n")])[0]
    ascii_art += my_shuffle([" ║  ╰┴┴┴╯  ║\n"," ║  ╭┴┼┴╮  ║\n"," ║  ╰╯v╰╯  ║\n", " ║  \___/  ║\n", " ║  ╰_-_╯  ║\n", " ║  ╰┬┬┬╯  ║\n", " ║  ╰v─v╯  ║\n", " ║  ╰───╯  ║\n", " ║  /|||\  ║\n", " ║  ╰┼┼┼╯  ║\n"," ║  \\vvv/  ║\n", " ║  \/v\/  ║\n", (" ║" + my_shuffle(["  ╰┴", "  ╰┬", "  \_", "  ╰v","  ╰─", "  /|", "  ╰┼", "  \/"])[0] + my_shuffle(["─","┴", "_", "v", "┼", "┬"])[0] + my_shuffle(["┴╯  ", "┬╯  ", "_/  ", "v╯  ","─╯  ", "|\  ", "┼╯  ", "\/  "])[0] + "║\n")])[0]
    ascii_art += my_shuffle(["┌╚═════════╝",  "┌╚═════════╝",  "┌╚═════════╝",   "┌╚═════════╝",   "┌╚═════════╝",   "┌╚═════════╝",   "┌╚═════════╝",   "┌╚═════════╝─ R","┌╚═════════╝─ R","┌╚═════════╝─ R","┌╚═════════╝─ SR","┌╚═════════╝─ SR","┌╚═════════╝─ " + my_shuffle(["", "", "S", "", "", "S", "", "", "SS"])[0] + my_shuffle(["", "S", "", "", "S", "", "", "S", "", "", "SS"])[0] + "R"])[0]

    return ascii_art

def custom_print(text, output_to_export):
    print(text)
    output_to_export += text + "\n"
    return output_to_export

def muh_gen(names_to_gen = 666, name_len_min = 3, name_len_max = 5, traits_min_count = 2, traits_max_count = 4):

    name_parts = ["жу", "жи", "жож", "жзе", "жа", "зо", "зи", "жзо", "му", "миж", "жо", "зму", "жим", "жом", "бжо", "бжу", "жю", "зю", "шу", "шиж"]
    possible_traits = [
    ["добрая", "нейтральная", "злая", "агрессивная", "спокойная"],
    ["крошечная", "маленькая", "небольшая", "крупная", "большая", "огромная", "гигантская"],
    ["хилая", "слабая", "сильная", "мощная", "могущественная"],
    ["тупая", "глупая", "смекалистая", "умная", "мудрая"],
    ["уродливая", "некрасивая", "красивая", "прекрасная"],
    ["чёрная", "серая", "коричневая", "бардовая", "зелёная", "белая", "тёмно серая"],
    ["очень медленная", "медленная", "медлительная", "ловкая", "очень ловкая", "быстрая", "очень быстрая", "сверх скоростная"],
    ["полудохлая", "раненая", "живучая", "неубиваемая", "быстро устаёт", "выносливая"],
    ["невкустная", "вкусная", "деликатесс", "мясистая", "жирненькая"],
    ["устойчива к ядам", "устойчива к магии", "устойчива к проклятьям", "устойчива к болезням", "уязвима к ядам", "уязвима к магии", "уязвима к проклятьям", "уязвима к болезням"],
    ["не помнит своё имя", "отвратительная память", "плохая память", "хорошая память", "фотографическая память"],
    ]

    file_name = "flys.txt"
    generated_names = []
    output_to_export = ""

    for i in range(names_to_gen):
        name = ""
        for j in range(random.randint(name_len_min, name_len_max)):
            name += name_parts[random.randint(0, len(name_parts) - 1)]

        while name in generated_names:
            name += name_parts[random.randint(0, len(name_parts) - 1)]

        name = name.capitalize()
        generated_names.append(name)

    output_to_export = custom_print("---- " + str(names_to_gen) + " мух ---- \n", output_to_export )

    for i in range(names_to_gen):
        output_to_export = custom_print(fly_ascii_face_gen(), output_to_export)

        output_to_export = custom_print("├ Муха " + str(i + 1) + ": " + generated_names[i], output_to_export)

        this_fly_traits = []
        this_fly_possible_traits = possible_traits.copy()

        for j in range(random.randint(traits_min_count, traits_max_count)):
            random.shuffle(this_fly_possible_traits)
            this_fly_traits.append(this_fly_possible_traits[0][random.randint(0, len(this_fly_possible_traits[0]) - 1)])
            this_fly_possible_traits.remove(this_fly_possible_traits[0])

        traits_string = "└─> "
        for trait in this_fly_traits:
            traits_string += trait + ", "

        output_to_export = custom_print(traits_string[:-2] + "\n", output_to_export)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join(script_dir, file_name)

    with open(relative_path, "w", encoding='utf-8') as f:
        f.write(output_to_export)

def video_splice():
    set_ffmpeg_paths("C:\\Users\\Limofeus\\AppData\\Local\\ffmpegio\\ffmpeg-downloader\\ffmpeg\\bin\\ffmpeg.exe")
    export_path = pathlib.Path(__file__).parent.resolve()

    video_url = str(input("Введите URl видео: "))

    downloaded_audio = download_video_as_audio(video_url, export_path)
    converted_audio = convert_to_wav(downloaded_audio)

    split_audio_path = str(export_path) + "\\splitAudio"
    renamed_audio_path = str(export_path) + "\\renamedAudio"
    ready_audio_path = str(export_path) + "\\readyAudio"

    split_audio(converted_audio, split_audio_path)
    recognize_audio(split_audio_path, renamed_audio_path)
    trim_audio(renamed_audio_path, ready_audio_path)

    print("Аудио нарезано и распознано...")

def main():
    print("Выберите функцию:\n1. Нарезка видео\n2. Генерация мух")
    user_choice = int(input())
    if user_choice == 1:
        video_splice()
    elif user_choice == 2:
        muh_gen()
    else:
        print("Неправильное значение!")

if __name__=='__main__':
    main()

