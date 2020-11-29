def sphinx(audio):
    try:
        print("-------------Sphinx successfully recognized the audio ---------")
        return r.recognize_sphinx(audio)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

def main():
    sphinx()
main()
