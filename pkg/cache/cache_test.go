package cache

import (
	"testing"
)

func TestCache(t *testing.T) {
	cases := []struct {
		key   string
		value string
	}{
		{"hello", "world"},
		{"key", ""},
		{"", "value"},
	}

	cache := NewCache()
	for _, c := range cases {
		cache.Insert(c.key, c.value)
		if !cache.Exists(c.key) {
			t.Fatalf("key '%s' does not exist in the cache after Insert", c.key)
		}
		value := cache.Get(c.key)
		if value != c.value {
			t.Fatalf("value '%s' does not match expected value '%s'", value, c.value)
		}
		cache.Delete(c.key)
		if cache.Exists(c.key) {
			t.Fatalf("key '%s' still exists in the cache after Delete", c.key)
		}
	}
}
