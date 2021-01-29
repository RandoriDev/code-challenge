package filter

import "github.com/gin-gonic/gin"

type BaseFilter interface {
	Apply(c *gin.Context)
}
