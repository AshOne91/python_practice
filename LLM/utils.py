def advanced_cot_template(client,query):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system","content": "you are advenced resoning system" },
            {"role": "user","content": f"""
            다음 문제를 단계별로 풀어주세요, 답변 후 스스로 검토해 오류를 수정하세요, 400자이내로 답변하세요.
            {query}
            1. 변수 정의.
            2. 방정식 설정.
            3. 계산 과정.
            4. 검토.
            5. 최종답변은 "사과: x원, 오렌지: x원" 형식으로 작성하세요.
            """}
                
        ],
        max_tokens=400,
        temperature = 0.7
    )
    return response.choices[0].message.content


def few_shot_cot(client,query):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system","content": "you are few shot resoning system" },
            {"role": "user","content": f"""
            다음 문제를 few shot으로 단계별로 풀어주세요, 아래 예제를 참고해 단계별로 답변하세요. 
            답변 후 스스로 검토해 오류를 수정하세요
            
             
            예제 1 : 한 농부가 닭과 소를 합쳐 20마리 키운다, 다리 수는 50개이다 닭과 소는 각각 몇 마리인가?
            1. 문제 분석: 문제에서는 닭과 소의 총 마리 수와 다리 수가 주어졌다. 닭과 소의 수를 구하는 것이 목표이다.
            2. 계산 단계: 닭을 D, 소를 C라고 하면 D + C = 20이고, 2D + 4C = 50 두 방정식을 풀어야 한다.
            3. 초기 답변: 닭은 10마리, 소는 10마리이다.
            4. 검토: 방정식을 풀면 닭은 15마리, 소는 5마리이다. 초기 답변이 틀렸다.
            5. 최종 답변: 닭은 15마리, 소는 5마리이다. 답을 수정했다. 
             
            예제 2 : 사과 3개와 오렌지 2개는 13,000원 사과 2개와 오렌지 3개는 12,000원, 사과와 오렌지는 각각 얼마인가? 
            1. 변수 정의: 
                - 사과의 가격을 x원, 오렌지의 가격을 y원이라고 정의합니다.
            2. 방정식 설정:
                - 3x + 2y = 13000 (사과 3개와 오렌지 2개의 가격 합은 13,000원)
                - 2x + 3y = 12000 (사과 2개와 오렌지 3개의 가격 합은 12,000원)
            3. 계산 과정:
                - 위 두 방정식을 풀어서 x와 y의 값을 구합니다.
                - 3x + 2y = 13000을 2배 해서 6x + 4y = 26000과 2x + 3y = 12000을 더해주면 5x + 7y = 38000이 됩니다.
                - 이를 풀면 x = 4000원, y = 3000원이 나옵니다.
            4. 검토:
                - 위 방정식에 x = 4000원, y = 3000원을 대입하여 원래 방정식을 만족하는지 확인합니다.
            5. 최종답변: "사과: 4000원, 오렌지: 3000원" 

            이제 문제 풀기 
            {query}
            1. 변수 정의.
            2. 방정식 설정.
            3. 계산 과정.
            4. 검토.
            5. 최종 답변.
            """}
                
        ],
        max_tokens=400,
        temperature = 0.7
    )
    return response.choices[0].message.content
