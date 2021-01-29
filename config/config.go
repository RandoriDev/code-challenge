package config

import (
	"fmt"
	"time"
)

type Config struct {
	Proxy *ProxyTarget
	AppPort string
	Filters *Filters
}

type ProxyTarget struct {
	DomainName  string
	Port  string
	Scheme string
}

type Filters struct {
	DelayRequestSeconds time.Duration
	CleanupVisitorsExpirationMinutes time.Duration
	SamplingScheduleMinutes time.Duration
}

// GetConfig returns in memory preset configs
func GetConfig() *Config {
	return &Config{
		Proxy: &ProxyTarget {
			DomainName:  "localhost",
			Port:  ":3000",
			Scheme: "http",
		},
		AppPort: ":8080",
		Filters: &Filters{
			DelayRequestSeconds: 2,
			CleanupVisitorsExpirationMinutes: 10,
			SamplingScheduleMinutes: 1,
		},
	}
}

// GetProxyTargetURL returns proxy target URL
func GetProxyTargetURL() string {
	return fmt.Sprintf("%s%s", GetConfig().Proxy.DomainName, GetConfig().Proxy.Port)
}

func GetDelayRequestSeconds() time.Duration  {
	return GetConfig().Filters.DelayRequestSeconds
}

func GetCleanupVisitorsExpirationMinutes() time.Duration  {
	return GetConfig().Filters.CleanupVisitorsExpirationMinutes
}

func GetSamplingScheduleMinutes() time.Duration  {
	return GetConfig().Filters.SamplingScheduleMinutes
}
