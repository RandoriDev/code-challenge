package logger

import (
	"log"
	"os"
	"sync"
)

type Object struct {
	Logger *log.Logger
	mutex  sync.Mutex
}

type CannotOpenLogFileException struct {
	Inner string
}

func (e *CannotOpenLogFileException) Error() string {
	return "Cannot open log file!"
}

func (l *Object) Start() error {
	openLogfile, err := os.OpenFile("data.log", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)

	if err != nil {
		return &CannotOpenLogFileException{
			Inner: err.Error(),
		}
	}

	l.Logger = log.New(openLogfile, "- \t\t", log.Ldate|log.Ltime|log.Lshortfile)

	return nil
}

func (l *Object) LogToFile(message string) {
	l.mutex.Lock()
	defer l.mutex.Unlock()

	l.Logger.Println(message)
}
