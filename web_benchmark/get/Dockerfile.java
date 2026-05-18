FROM openjdk:17-slim

WORKDIR /app
COPY server.java .

# Download JSON library (org.json)
RUN apt-get update && apt-get install -y wget maven && \
    echo 'import org.json.JSONObject;' > /tmp/test.java

COPY server.java .

ENV PORT=8080
EXPOSE 8080

RUN javac -cp /usr/share/java/* server.java 2>/dev/null || \
    (cd /tmp && wget -q https://repo1.maven.org/maven2/org/json/json/20230227/json-20230227.jar && \
     cp json-20230227.jar /tmp/json.jar && \
     cd /app && javac -cp /tmp/json.jar server.java)

CMD ["java", "-cp", "/tmp/json.jar:.", "server"]
