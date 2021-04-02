package clientshandler

import "sync"

type Object struct {
	clients map[string]string
	mutex   sync.Mutex
}

func (c *Object) Start() {
	c.clients = make(map[string]string)
}

func (c *Object) processClientMessage(ip, message string) {
	c.mutex.Lock()
	defer c.mutex.Unlock()

	c.clients[ip] = message
}

func (c *Object) ShouldDelay(ip, message string) bool {
	c.mutex.Lock()
	_, ok := c.clients[ip]
	c.mutex.Unlock()

	if ok {
		return c.clients[ip] == message
	} else {
		c.processClientMessage(ip, message)

		return false
	}
}
