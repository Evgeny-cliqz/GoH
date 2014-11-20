package main

import (
	"log"
    "fmt"
    "net/http"
    "io/ioutil"
    "encoding/json"
    "time"
)

//test version of logs
var GoLogs map[uint64]Signal

//
var Count uint64

//struct. for the signal json
type Signal struct
	{
	Metrics map[string]string

	Timestamp time.Time

	State string

	Id map[string]string

	Periodicity string
}

//struct. for the response json
type RespMessage struct
{
	Message string	
}

func handler(w http.ResponseWriter, req *http.Request) {
	//decode message
	body, err := ioutil.ReadAll(req.Body)
    if err != nil {
        log.Println("I/O error")
    }
    
    //read signal json
    var s Signal
    err = json.Unmarshal(body, &s)
    if err != nil {
        log.Println("Json decode error!")
        log.Println(err)
    }

    log.Println(string(body))
    

    //send response
    m, err := json.Marshal(RespMessage{"OK"})
    if err != nil {
        log.Println("json write error")
    }
    
    //save a log
    if (GoLogs == nil){
    	Count = 0
    	GoLogs = make(map[uint64]Signal)    
    }

    Count++
    

    GoLogs[Count] = s
    log.Println(len(GoLogs))

	fmt.Fprintf(w, string(m))

}

func main() {

    http.HandleFunc("/", handler)
    http.ListenAndServe(":8080", nil)
}