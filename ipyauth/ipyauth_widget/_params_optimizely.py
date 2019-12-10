import json

from copy import deepcopy as copy
from traitlets import HasTraits, Unicode, validate, TraitError

from ._util import Util


class ParamsOptimizely(HasTraits):
    """
    Optimizely OAuth Documentation https://developers.optimizely.com/x/authentication/oauth/
    """

    name = Unicode()
    response_type = Unicode()
    client_id = Unicode()
    redirect_uri = Unicode()
    scope = Unicode()

    def __init__(
        self,
        name="optimizely",
        response_type=None,
        client_id=None,
        redirect_uri=None,
        scope=None,
        dotenv_folder=".",
        dotenv_file=None,
    ):
        """
        Initializes the class with a config .env file and optional
        params to override the config
        """
        dic = Util.load_dotenv(dotenv_folder, dotenv_file, name)

        for k, v in dic.items():
            setattr(self, k, v)

        self.name = name

        if response_type:
            self.response_type = response_type
        if client_id:
            self.client_id = client_id
        if redirect_uri:
            self.redirect_uri = redirect_uri
        if scope:
            self.scope = scope

        self.data = self.build_data()

    def to_dict(self):
        """
        Returns a dictionary representation of the parameters set during instance initalization
        """
        d = copy(self.__dict__)
        d = {k: v for k, v in d.items() if v is not None}
        return d

    @validate("response_type")
    def _valid_response_type(self, proposal):
        """
        Checks that the response_type value is equal to "token",
        which is used for OAuth Implicit Grant
        """
        if not proposal["value"] == "token":
            raise TraitError('response_type must be "token"')
        return proposal["value"]

    @validate("redirect_uri")
    def _valid_redirect_uri(self, proposal):
        """
        Checks that the redirect_uri is a valid URL
        """
        if not Util.is_url(proposal["value"]):
            raise TraitError("redirect_uri must be a url")
        return proposal["value"]

    def build_data(self):
        """
        Returns a dictionary of the passed in parameters
        """
        props_params = ["name"]
        props_url_params = ["response_type", "client_id", "redirect_uri", "scope"]

        data = {}
        for k in props_params:
            v = getattr(self, k)
            if v != "":
                data[k] = v

        data_url = {}
        for k in props_url_params:
            v = getattr(self, k)
            if v != "":
                data_url[k] = v

        data["url_params"] = data_url

        return data
