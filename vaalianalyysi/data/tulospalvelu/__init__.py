from vaalianalyysi.data.tulospalvelu import dl
from vaalianalyysi.data.tulospalvelu import df
from vaalianalyysi.data.tulospalvelu.vaalit import Alue
from vaalianalyysi.data.tulospalvelu.vaalit import Kunta
from vaalianalyysi.data.tulospalvelu.vaalit import Puolue
from vaalianalyysi.data.tulospalvelu.vaalit import Vaalit


def vaalit(*args, **kwargs):
    return Vaalit(*args, **kwargs)
