"""
# Riot Library - Data Transfer Objects
Houses DTO classes returned from Riot API requests. 
This library is intended to work with API's from Riot as of 12/23/2024
"""
from json import dumps, loads, load

# helper functions
def _combine_args(*args: dict):
        arguments = {}
        for arg in [a for a in args if a is not None]:
            arguments.update(arg)
        return arguments

# DTOs
class GenericDto:
    def __init__(self, name: str, arg: dict = None, **kwargs):
        """Generic Data Transfer Object class

        Args:
            name (str): The name of the Dto.
        """
        self.name = name
        self.dto = _combine_args(arg, kwargs)

    def __str__(self):
        return "\n".join((
            self.name,
            dumps(self.dto)
        ))
    
    def __getitem__(self, key):
        return super().__getitem__(self, key)
    
    def __setitem__(self, key, value):
        super().__setitem__(self, key, value)

class SummonerDto(GenericDto):
    def __init__(self, arg: dict = None, **kwargs):
        """
        API reference: https://developer.riotgames.com/apis#summoner-v4/GET_getByPUUID
        """
        args = _combine_args(arg, kwargs)
        super().__init__(self, "SummonerDto", args)

class BanDto(GenericDto):
    def __init__(self, arg: dict = None, **kwargs):
        """
        API reference: https://developer.riotgames.com/apis#match-v5/GET_getMatch
        """
        args = _combine_args(arg, kwargs)
        super().__init__(self, "BanDto", args)

class ObjectiveDto(GenericDto):
    def __init__(self, arg: dict = None, **kwargs):
        """
        API reference: https://developer.riotgames.com/apis#match-v5/GET_getMatch
        """
        args = _combine_args(arg, kwargs)
        super().__init__(self, "ObjectiveDto", args)

class ObjectivesDto(GenericDto):
    def __init__(self, arg: dict = None, **kwargs):
        """
        API reference: https://developer.riotgames.com/apis#match-v5/GET_getMatch
        """
        args = _combine_args(arg, kwargs)
        args = {k: ObjectiveDto(v) for k, v in args.items()}
        super().__init__(self, "ObjectivesDto", args)

class TeamDto(GenericDto):
    def __init__(self, arg: dict = None, **kwargs):
        """
        API reference: https://developer.riotgames.com/apis#match-v5/GET_getMatch
        """
        args = _combine_args(arg, kwargs)
        args["bans"] = [BanDto(b) for b in args["bans"]]
        args["objectives"] = ObjectivesDto(args["objectives"])
        super().__init__(self, "TeamDto", args)

class ChallengesDto(GenericDto):
    def __init__(self, arg: dict = None, **kwargs):
        """
        API reference: https://developer.riotgames.com/apis#match-v5/GET_getMatch
        """
        args = _combine_args(arg, kwargs)
        super().__init__(self, "ChallengesDto", args)

class MissionsDto(GenericDto):
    def __init__(self, arg: dict = None, **kwargs):
        """
        API reference: https://developer.riotgames.com/apis#match-v5/GET_getMatch
        """
        args = _combine_args(arg, kwargs)
        super().__init__(self, "MissionsDto", args)

class PerkStatsDto(GenericDto):
    def __init__(self, arg: dict = None, **kwargs):
        """
        API reference: https://developer.riotgames.com/apis#match-v5/GET_getMatch
        """
        args = _combine_args(arg, kwargs)
        super().__init__(self, "PerkStatsDto", args)

class PerkStyleSelectionDto(GenericDto):
    def __init__(self, arg: dict = None, **kwargs):
        """
        API reference: https://developer.riotgames.com/apis#match-v5/GET_getMatch
        """
        args = _combine_args(arg, kwargs)
        super().__init__(self, "PerkStyleSelectionDto", args)

class PerkStyleDto(GenericDto):
    def __init__(self, arg: dict = None, **kwargs):
        """
        API reference: https://developer.riotgames.com/apis#match-v5/GET_getMatch
        """
        args = _combine_args(arg, kwargs)
        args["selections"] = [PerkStyleSelectionDto(s) for s in args["selections"]]
        super().__init__(self, "PerkStyleDto", args)

class PerksDto(GenericDto):
    def __init__(self, arg: dict = None, **kwargs):
        """
        API reference: https://developer.riotgames.com/apis#match-v5/GET_getMatch
        """
        args = _combine_args(arg, kwargs)
        args["statPerks"] = PerkStatsDto(args["statPerks"])
        args["styles"] = [PerkStyleDto(s) for s in args["styles"]]
        super().__init__(self, "PerksDto", args)

class ParticipantDto(GenericDto):
    def __init__(self, arg: dict = None, **kwargs):
        """
        API reference: https://developer.riotgames.com/apis#match-v5/GET_getMatch
        """
        args = _combine_args(arg, kwargs)
        args["challenges"] = ChallengesDto(args["challenges"])
        args["missions"] = MissionsDto(args["missions"])
        args["perks"] = PerksDto(args["perks"])
        super().__init__(self, "ParticipantDto", args)

class MetadataDto(GenericDto):
    def __init__(self, arg: dict = None, **kwargs):
        """
        API reference: https://developer.riotgames.com/apis#match-v5/GET_getMatch
        """
        args = _combine_args(arg, kwargs)
        super().__init__(self, "MetadataDto", args)

class InfoDto(GenericDto):
    def __init__(self, arg: dict = None, **kwargs):
        """
        API reference: https://developer.riotgames.com/apis#match-v5/GET_getMatch
        """
        args = _combine_args(arg, kwargs)
        args["participants"] = [ParticipantDto(p) for p in args["participants"]]
        args["teams"] = [TeamDto(t) for t in args["teams"]]
        super().__init__(self, "InfoDto", args)

class MatchDto(GenericDto):
    def __init__(self, arg: dict = None, **kwargs):
        """
        API reference: https://developer.riotgames.com/apis#match-v5/GET_getMatch
        """
        args = _combine_args(arg, kwargs)
        args["metadata"] = MetadataDto(args["metadata"])
        args["info"] = InfoDto(args["info"])
        super().__init__(self, "MatchDto", args)