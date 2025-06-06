FROM public.ecr.aws/amazoncorretto/amazoncorretto:17-al2023-headless

# Download GitBucket
ADD https://github.com/gitbucket/gitbucket/releases/download/4.42.1/gitbucket.war /opt/gitbucket.war

# Set up GitBucket home directory
ENV GITBUCKET_HOME /var/gitbucket
RUN mkdir -p $GITBUCKET_HOME
VOLUME $GITBUCKET_HOME

# Port for web page and Port for SSH access to git repository
EXPOSE 8080 29418

# Start GitBucket
CMD ["sh", "-c", "java ${JAVA_OPTS} -jar /opt/gitbucket.war"]
