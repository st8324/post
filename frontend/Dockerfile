# -------------------------
# 1단계: React 빌드
# -------------------------
FROM node:18 AS frontend

WORKDIR /frontend
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# 2단계: Nginx 실행
FROM nginx:alpine
# 기본 Nginx 설정 삭제
RUN rm /etc/nginx/conf.d/default.conf
# 커스텀 Nginx 설정 복사 (아래에서 만들 파일)
COPY nginx.conf /etc/nginx/conf.d/

# 리액트 빌드 결과물을 Nginx 서빙 폴더로 복사
COPY --from=build /frontend/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]