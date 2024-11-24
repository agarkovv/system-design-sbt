Вот объединенный файл `README.md`, который включает все шаги, выполненные в проекте, и инструкции для автоматизации сборки и деплоя приложения через Jenkins:


# Автоматизация сборки и деплоя приложения с помощью Jenkins

Приложение: https://github.com/agarkovv/example-sentiment-project

В этом проекте была выполнена автоматизация процесса сборки, тестирования и деплоя приложения с использованием Jenkins. Целью было создать пайплайн Jenkins для автоматической сборки и тестирования при событиях pull-request/push. В проекте использовалась интеграция с SonarQube для анализа кода и Allure для генерации отчетов о тестах. Также был настроен деплой через Docker.

## Шаги, проделанные в проекте:

### 1. Настройка Jenkins Pipeline для автоматической сборки
Создан Jenkins pipeline, который выполняет следующие шаги:
- **Сборка приложения** с использованием `docker-compose` для запуска необходимых сервисов и сборки контейнера.
- **Запуск автотестов** с использованием фреймворка `pytest` для юнит-тестирования.
- **Сборка отчета Allure** на основе результатов тестов и отправка отчета в Jenkins.
- **Анализ исходного кода** с помощью SonarQube с целью улучшения качества кода и обеспечения покрытия тестами не менее 90%.
- **Деплой приложения** через Docker, с использованием `docker-compose` для разворачивания контейнеров.

### 2. Проблемы с доступом к Docker
На этапе конфигурации Jenkins контейнера для работы с Docker возникли проблемы с правами доступа к сокету Docker. Для их решения были выполнены следующие действия:
- Убедились, что пользователь `jenkins` добавлен в группу `docker` для получения доступа к сокету Docker.
- Настроили правильные права доступа для сокета Docker через команду:
  ```bash
  chmod 666 /var/run/docker.sock
  ```
  Это обеспечило возможность Jenkins контейнеру взаимодействовать с Docker.

### 3. Конфигурация SonarQube для анализа кода
Был настроен SonarQube для автоматического анализа кода в процессе сборки:
- Использовали SonarQube для анализа качества кода с целью выявления ошибок и обеспечения покрытия тестами.
- Настроили SonarQube для работы с Maven или другими инструментами сборки, в зависимости от проекта.
- Исправили ошибки в коде, добившись не менее 90% покрытия тестами.

### 4. Интеграция Allure для отчетности по тестам
Для генерации отчетов о результатах тестов была интегрирована библиотека Allure:
- На каждом этапе пайплайна после выполнения тестов создавался отчет в формате Allure.
- Отчет отображался в Jenkins, что позволяло легко отслеживать результаты тестирования.

### 5. Docker для деплоя приложения
Для деплоя приложения использовался Docker:
- С помощью `docker-compose` были развернуты необходимые сервисы, включая базу данных и приложение.
- Создан контейнер для приложения с настроенным доступом к Docker сокету для управления контейнерами через Jenkins.

### Пример конфигурации Jenkinsfile:

```groovy
pipeline {
    agent any
    environment {
        SONARQUBE = 'SonarQube'
        SONARQUBE_TOKEN = credentials('sonarqube-token')
        ALLURE_RESULTS = "allure-results"
        TEST_REPORTS = "target/test-*.xml"
    }
    stages {
        stage('Clone repository') {
            steps {
                git branch: 'main', url: 'https://github.com/agarkovv/example-sentiment-project'
            }
        }
        stage('Build Application') {
            steps {
                script {
                    sh "docker-compose -f docker-compose.yml build"
                }
            }
        }
        stage('Run Unit Tests') {
            steps {
                script {
                    sh "pytest --maxfail=1 --disable-warnings -q"
                }
            }
        }
        stage('SonarQube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('SonarQube') {
                        sh 'mvn sonar:sonar'
                    }
                }
            }
        }
        stage('Generate Allure Report') {
            steps {
                script {
                    sh "allure serve ${ALLURE_RESULTS}"
                }
            }
        }
        stage('Deploy Application') {
            steps {
                script {
                    sh "docker-compose -f docker-compose.yml up -d"
                }
            }
        }
    }
    post {
        always {
            junit '**/target/test-*.xml'
            allure results: ['**/allure-results']
        }
        success {
            echo 'Build, test, and deploy succeeded!'
        }
        failure {
            echo 'Something went wrong during the pipeline.'
        }
    }
}
```

## Требования:
- Установленный Jenkins с плагинами для работы с Docker, SonarQube, Allure и другими необходимыми инструментами.
- Доступ к Docker в Jenkins контейнере.
- Настроенный SonarQube сервер для анализа кода.
