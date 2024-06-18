class Help:
    def dice_help():
        # TODO: implement help for dice commands
        return
    
    def news_help():
        # TODO: implement help for news commands
        return

    def help_processor(attributes: list[str]) -> str:
        general_help_text = "COMING SOON"

        if len(attributes) == 1:
            return general_help_text
        
        match attributes[0]:
            case _:
                return "COMING SOON"