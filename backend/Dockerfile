# -------------------------
# 2단계: Spring 빌드
# -------------------------
FROM gradle:8-jdk21 AS backend-build

WORKDIR /backend
COPY . .

RUN chmod +x gradlew
RUN ./gradlew build -x test --no-daemon


# -------------------------
# 3단계: 실행용 이미지
# -------------------------
FROM eclipse-temurin:21-jre

WORKDIR /backend
COPY --from=backend-build /app/build/libs/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-Xmx512m","-jar", "app.jar"]
