from django_unicorn.components import UnicornView


class WorldView(UnicornView):
    def mount(self):
        arg = self.component_args[0]
        kwarg = self.component_kwargs["name"]

        assert f"{arg} {kwarg}" == "Hello Galaxy"
