def test_ping(test_app):
    # when
    response = test_app.get("/ping")

    # then
    assert response.status_code == 200
    assert response.json() == {"environment": "dev", "ping": "pong!", "testing": True}

    # Ao escrever testes, tente seguir a estrutura Given-When-Then para ajudar a tornar o processo de escrita de testes
    # mais fácil e rápido. Também ajuda a comunicar melhor o objetivo de seus testes, para que seja mais fácil de ler por
    # você e pelos outros no futuro.


# Given o estado do aplicativo antes da execução do teste

# When o comportamento/lógica que está sendo testado

# Then as mudanças esperadas com base no comportamento
