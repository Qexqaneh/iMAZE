FROM gcc:5.3.0

COPY ./src /usr/src/imaze

WORKDIR /usr/src/imaze

#RUN gcc -o main main.cpp
RUN g++ main.cpp -std=c++11 -o main

CMD ["./main"]
