# -------------------------
# 1단계: React 빌드
# -------------------------
FROM node:18 AS frontend

WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
RUN npm run build


# -------------------------
# 2단계: Spring 빌드
# -------------------------
FROM gradle:8-jdk21 AS backend-build

WORKDIR /backend
COPY backend/ .

# React build 결과를 Spring static에 복사
COPY --from=frontend /frontend/build ./src/main/resources/static

RUN chmod +x gradlew
RUN ./gradlew build --no-daemon


# -------------------------
# 3단계: 실행용 이미지
# -------------------------
FROM eclipse-temurin:21-jre

WORKDIR /app
COPY --from=backend-build /backend/build/libs/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-Xmx512m","-jar", "app.jar"]
