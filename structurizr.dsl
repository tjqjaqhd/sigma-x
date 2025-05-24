workspace "SIGMA Trading System" "Architecture for the SIGMA Trading System" {
    model {
        user = person "Trader" "A user who interacts with the trading system."

        softwareSystem = softwareSystem "SIGMA Trading System" "The core trading system."
        user -> softwareSystem "Uses"

        containerApi = container softwareSystem "API" "Provides external access to the trading system."
        containerCore = container softwareSystem "Core" "Handles trading logic and risk management."
        containerDb = container softwareSystem "Database" "Stores trading data."

        user -> containerApi "Interacts with"
        containerApi -> containerCore "Delegates to"
        containerCore -> containerDb "Reads/Writes"
    }

    views {
        systemContext softwareSystem {
            include *
            autolayout lr
        }

        container softwareSystem {
            include *
            autolayout lr
        }

        theme default
    }
}
