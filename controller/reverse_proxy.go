package controller

import (
	"github.com/gin-gonic/gin"
	"github.com/santiagomoranlabat/da-api/config"
	"net/http"
	"net/http/httputil"
	"net/url"
	"strings"
	"github.com/sirupsen/logrus"
)

type ReverseProxy struct{}

// GetOne creates a reverseProxy and proxies the request to target api
func (t *ReverseProxy) GetOne(c *gin.Context) {
	targetURL := config.GetProxyTargetURL()
	logrus.Infof("Beginning of transaction from host: %s, redirecting to %s, method: %s", c.Request.Host, targetURL, c.Request.Method)
	origin, _ := url.Parse(config.GetProxyTargetURL())
	reverseProxy := httputil.NewSingleHostReverseProxy(origin)

	reverseProxy.Director = func(req *http.Request) {
		req.Header = c.Request.Header
		req.URL.Scheme = "http"
		req.URL.Host = targetURL
		req.URL.Path = getProxyPath(origin.Path, req.URL.Path)
	}

	reverseProxy.ErrorHandler = func(http.ResponseWriter, *http.Request, error) {
		logrus.Fatalf("ReverseProxy incomplete. From host: %s, to %s, method: %s", c.Request.Host, targetURL, c.Request.Method)

	}

	reverseProxy.ServeHTTP(c.Writer, c.Request)

	logrus.Infof("ReverseProxy successful. From host: %s, to %s", c.Request.Host, targetURL)
}

// getProxyPath returns the proxy path as string
func getProxyPath(originPath string, requestPath string) string {
	wildcardIndex := strings.IndexAny("/*path", "*")
	proxyPath := singleJoiningSlash(originPath, requestPath[wildcardIndex:])
	if strings.HasSuffix(proxyPath, "/") && len(proxyPath) > 1 {
		proxyPath = proxyPath[:len(proxyPath)-1]
	}
	return proxyPath
}

// singleJoiningSlash returns a the path with slash
func singleJoiningSlash(a, b string) string {
	aslash := strings.HasSuffix(a, "/")
	bslash := strings.HasPrefix(b, "/")
	switch {
	case aslash && bslash:
		return a + b[1:]
	case !aslash && !bslash:
		return a + "/" + b
	}
	return a + b
}
