package cache

import "sync"

type Cache struct {
	sync.Mutex
	store map[string]string
}

func NewCache() *Cache {
	c := Cache{
		store: map[string]string{},
	}
	return &c
}

func (c *Cache) Insert(key string, value string) {
	c.store[key] = value
}

func (c *Cache) Get(key string) string {
	return c.store[key]
}

func (c *Cache) Exists(key string) bool {
	_, ok := c.store[key]
	return ok
}

func (c *Cache) Delete(key string) {
	delete(c.store, key)
}
