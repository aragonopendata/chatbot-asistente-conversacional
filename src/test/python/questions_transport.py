import requests
import time
from cmd import *
from pprint import pprint

CHAT_ROOM_URL = "http://127.0.0.1:5000"

QUESTIONS_ANSWERS_TRANSPORT_TEXT = [
    {
        "¿a qué velocidad se puede ir por la carretera A-220?",
        "La velocidad máxima de la carretera A-220 es 90 kilómetros por hora."
    }, {
        "¿Qué tipo de carretera es la carretera A-220?",
        "La carretera A-220 es autonómica."
    }, {
        "¿Cuál es la descripción de la carretera A-220?",
        "La descripción de la carretera A-220 es La Almunia de Doña Godina por Cariñena a Belchite."
    }, {
        "¿Qué tipo de zonas hay cercanas a la carretera A-220?",
        "Los zonas cercanas a la carretera A-220 son:\n\t- Zona de dominio público"
    }, {
        "¿Qué puentes hay en la localidad de Cariñena?",
        "Los puentes que hay en Cariñena son:\n\t- 0A-0220-0016+500\n\t- 0A-0220-0021+060\n\t- 0A-0220-0021+250\n\t- 0A-0220-0026+700"
    }, {
        "En qué punto kilométrico se encuentra el puente de Cariñena?",
         "Los puentes de Cariñena se encuentran en los puntos kilométricos:\n\t- 16.500000 de la carretera A-220\n\t- 21.060000 de la carretera A-220\n\t- 21.250000 de la carretera A-220\n\t- 26.700000 de la carretera A-220"
    }, {
        "¿En qué puntos kilométricos se encuentran los puentes de la carretera A-220?",
        "Los puentes de la carretera A-220 están en los puntos kilométricos:\n\t- 16.500000\n\t- 21.060000\n\t- 21.250000\n\t- 26.700000\n\t- 37.600000"
    }, {
        "¿En qué localidades se encuentran los puentes de la carretera A-220?",
		 "Los puentes de la carretera A-220 están en las siguientes localidades:\n\t- CARIÑENA\n\t- VILLANUEVA DE HUERVA"
    }, {
        "¿Que longitud tiene la carretera A-220?",
        "La carretera A-220 tiene 67.50913694011999 kilómetros de longitud."
    }, {
        "¿Cuántos kilómetros tiene la carretera de Daroca a Belchite?",
        "La longitud de la carretera entre Daroca y Belchite es de 77.84 kilómetros"
    }
]

QUESTIONS_ANSWERS_TRANSPORT_LEN = [
    {
        "¿Qué carreteras hay en la provincia de Zaragoza?",
        2
    }, {
        "¿Por qué carreteras puedo llegar a Belchite?",
        2
    }, {
        "¿Qué puentes hay en la carretera A-220?",
        2
    }
]


def test_questions(question_text: list, question_len: list, results) -> None:
    """
    Test of chat room: connectivity, agent status and input processing
    """
    response = requests.get(CHAT_ROOM_URL)
    if response.status_code == 200:
        # print_passed("Chat room is running")
        print("Chat room is running")
    else:
        # print_failed("Error in administrator Flask server")
        print("Error in administrator Flask server")
        exit(-1)

    response_status = requests.get(CHAT_ROOM_URL + "/status")
    json_response = response_status.json()
    if json_response["status"] == 200:
        # print_passed("Chat room agent is running")
        print("Chat room agent is running")
    else:
        # print_failed("Error chat room agent, agent not ready")
        print("Error chat room agent, agent not ready")
        exit(-1)

    cookies_dict = response.cookies.get_dict()
    all_questions = [f"pregunta ','esperado','respondido','correcto'\n"]
    fails = 0
    passed = 0

    if cookies_dict:

        for element in question_text:
            question = list(dict(element).keys())[0]
            answer = element.get(question)
            response = requests.post(
                CHAT_ROOM_URL + "/chat",
                cookies=cookies_dict,
                json={"text": question, "timeout": False},
            )

            if response.status_code == 200:
                json_response = response.json()
                if len(json_response["answer"]) > 0 and answer.lower() in ("".join(json_response["answer"]).lower()):
                    #                    all_questions.append(f" '{question}' , '{answer}' ,'{''.join(json_response['answer'])}' ,{True} \n")
                    passed = passed + 1
                else:
                    all_questions.append(
                        f" '{question}' , '{answer}' ,'{''.join(json_response['answer'])}' ,{False} \n")
                    fails = fails + 1
                    # questions_fails.append({"pregunta":question , "esperado":answer , "respondido":" ".join(json_response["answer"]) })
            results.append([" ".join(json_response["answer"]), answer, fails])

        csv = ' '.join(all_questions)
        if fails == 0:
            # print_passed("Question OK")
            print("Question OK")

        else:
            # print_failed(f"Question all  , fails: {fails} of  {passed + fails}:\n {csv}")
            print(f"Question all  , fails: {fails} of  {passed + fails}:\n {csv}")

        fails = 0
        passed = 0
        all_questions = []

        for element in question_len:
            question = list(dict(element).keys())[0]
            answer = element.get(question)
            response = requests.post(
                CHAT_ROOM_URL + "/chat",
                cookies=cookies_dict,
                json={"text": question, "timeout": False},
            )

            if response.status_code == 200:
                json_response = response.json()
                if len(json_response["answer"]) > 0 and len("".join(json_response["answer"])) >= answer:
                    #                    all_questions.append(f" '{question}' , '{answer}' ,'{''.join(json_response['answer'])}' ,{True}")
                    passed = passed + 1
                else:
                    fails = fails + 1
                    all_questions.append(f" '{question}' , '{answer}' ,'{''.join(json_response['answer'])}' ,{False}")
                    # questions_fails.append({"pregunta":question , "esperado":answer , "respondido":" ".join(json_response["answer"]) })
                results.append([json_response["answer"], json_response["answer"], fails])

        if fails == 0:
            # print_passed("Question OK")
            print("Question OK")

        else:
            csv = ' '.join(all_questions)
            # print_failed(f"Question all , fails: {fails} of  {len(all_questions)}:\n {csv}")
            print(f"Question all , fails: {fails} of  {len(all_questions)}:\n {csv}")

    return results

if __name__ == "__main__":
    results = []
    results = test_questions(QUESTIONS_ANSWERS_TRANSPORT_TEXT,[],results)
    #results = test_questions(QUESTIONS_ANSWERS_TRANSPORT_LEN, [], results)
    print(str(results))