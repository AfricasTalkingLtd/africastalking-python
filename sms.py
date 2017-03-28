from africastalking.AfricasTalkingGateway import (AfricasTalkingGateway, AfricasTalkingGatewayException)

#create a gateway instance
gateway = AfricasTalkingGateway(
        username    = "jani",
        apiKey      = "d46192b5e6c1bdf6e24ae3760f5d49cde42e8b09d53f01fc929eec205996f5ce",
        environment = "sandbox"
)

gateway.sendMessage("+254787235065", "Hello......")
