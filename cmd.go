package main

import (
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
	"strings"
)

// Command-line helper library sets up cli commands and args
var rootCmd = &cobra.Command{
	Use:   "proxy",
	Short: "A Randori code challenge proxy",
	Run: func(cmd *cobra.Command, args []string) {
		startProxyServer()
	},
}

// Initialize cli/env arguments and defaults
func init() {
	rootCmd.PersistentFlags().StringP("listen-addr", "a", "127.0.0.1:8080", "Listen address")
	rootCmd.PersistentFlags().StringP("backend-url", "b", "http://127.0.0.1:8081", "The backend URL to proxy requests to. Must be in URL format.")
	viper.BindPFlag("listen-addr", rootCmd.PersistentFlags().Lookup("listen-addr"))
	viper.BindPFlag("backend-url", rootCmd.PersistentFlags().Lookup("backend-url"))
	viper.SetEnvKeyReplacer(strings.NewReplacer("-", "_"))
	viper.AutomaticEnv()
}
