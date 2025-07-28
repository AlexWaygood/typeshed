from _typeshed import Incomplete
from typing import ClassVar

from ..core import WesternCalendar

class Brazil(WesternCalendar):
    """Brazil"""

    FIXED_HOLIDAYS: Incomplete
    include_sao_jose: ClassVar[bool]
    sao_jose_label: ClassVar[str]
    include_sao_pedro: ClassVar[bool]
    sao_pedro_label: ClassVar[str]
    include_sao_joao: ClassVar[bool]
    sao_joao_label: ClassVar[str]
    include_labour_day: ClassVar[bool]
    include_servidor_publico: ClassVar[bool]
    servidor_publico_label: ClassVar[str]
    include_consciencia_negra: ClassVar[bool]
    consciencia_negra_day: Incomplete
    consciencia_negra_label: ClassVar[str]
    include_easter_sunday: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]
    immaculate_conception_label: ClassVar[str]
    def get_variable_days(self, year): ...

class BrazilAcre(Brazil):
    """Brazil Acre State"""

    FIXED_HOLIDAYS: Incomplete

class BrazilAlagoas(Brazil):
    """Brazil Alagoas State"""

    FIXED_HOLIDAYS: Incomplete
    include_sao_pedro: ClassVar[bool]
    include_sao_joao: ClassVar[bool]
    include_consciencia_negra: ClassVar[bool]

class BrazilAmapa(Brazil):
    """Brazil Amapá State"""

    FIXED_HOLIDAYS: Incomplete
    include_sao_jose: ClassVar[bool]
    sao_jose_label: ClassVar[str]
    include_consciencia_negra: ClassVar[bool]

class BrazilAmazonas(Brazil):
    """Brazil Amazonas State"""

    FIXED_HOLIDAYS: Incomplete
    include_consciencia_negra: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]

class BrazilBahia(Brazil):
    """Brazil Bahia State"""

    FIXED_HOLIDAYS: Incomplete

class BrazilCeara(Brazil):
    """Brazil Ceará State"""

    FIXED_HOLIDAYS: Incomplete
    include_sao_jose: ClassVar[bool]

class BrazilDistritoFederal(Brazil):
    """Brazil Distrito Federal State"""

    FIXED_HOLIDAYS: Incomplete

class BrazilEspiritoSanto(Brazil):
    """Brazil Espírito Santo State"""

    include_servidor_publico: ClassVar[bool]

class BrazilGoias(Brazil):
    """Brazil Goiás State"""

    include_servidor_publico: ClassVar[bool]

class BrazilMaranhao(Brazil):
    """Brazil Maranhão State"""

    FIXED_HOLIDAYS: Incomplete
    include_immaculate_conception: ClassVar[bool]

class BrazilMinasGerais(Brazil):
    """Brasil Minas Gerais State"""

    FIXED_HOLIDAYS: Incomplete

class BrazilMatoGrosso(Brazil):
    """Brazil Mato Grosso State"""

    include_consciencia_negra: ClassVar[bool]
    consciencia_negra_day: Incomplete

class BrazilMatoGrossoDoSul(Brazil):
    """Brazil Mato Grosso do Sul State"""

    FIXED_HOLIDAYS: Incomplete

class BrazilPara(Brazil):
    """Brazil Pará State"""

    FIXED_HOLIDAYS: Incomplete
    include_immaculate_conception: ClassVar[bool]

class BrazilParaiba(Brazil):
    """Brazil Paraíba State"""

    FIXED_HOLIDAYS: Incomplete

class BrazilPernambuco(Brazil):
    """Brazil Pernambuco State"""

    FIXED_HOLIDAYS: Incomplete
    include_sao_joao: ClassVar[bool]

class BrazilPiaui(Brazil):
    """Brazil Piauí State"""

    FIXED_HOLIDAYS: Incomplete

class BrazilParana(Brazil):
    """Brazil Paraná State"""

    FIXED_HOLIDAYS: Incomplete

class BrazilRioDeJaneiro(Brazil):
    """Brazil Rio de Janeiro State"""

    FIXED_HOLIDAYS: Incomplete
    include_fat_tuesday: ClassVar[bool]
    fat_tuesday_label: ClassVar[str]
    include_servidor_publico: ClassVar[bool]
    servidor_publico_label: ClassVar[str]
    include_consciencia_negra: ClassVar[bool]
    consciencia_negra_label: ClassVar[str]
    include_immaculate_conception: ClassVar[bool]
    def get_dia_do_comercio(self, year):
        """
        Return Dia do Comércio variable date

        It happens on the 3rd Monday of october.
        """

    def get_variable_days(self, year): ...

class BrazilRioGrandeDoNorte(Brazil):
    """Brazil Rio Grande do Norte State"""

    FIXED_HOLIDAYS: Incomplete
    include_sao_pedro: ClassVar[bool]
    sao_pedro_label: ClassVar[str]

class BrazilRioGrandeDoSul(Brazil):
    """Brazil Rio Grande do Sul State"""

    FIXED_HOLIDAYS: Incomplete

class BrazilRondonia(Brazil):
    """Brazil Rondônia State"""

    FIXED_HOLIDAYS: Incomplete

class BrazilRoraima(Brazil):
    """Brazil Roraima State"""

    FIXED_HOLIDAYS: Incomplete

class BrazilSantaCatarina(Brazil):
    """Brazil Santa Catarina State"""

    FIXED_HOLIDAYS: Incomplete

class BrazilSaoPauloState(Brazil):
    """Brazil São Paulo State"""

    FIXED_HOLIDAYS: Incomplete

class BrazilSaoPauloCity(BrazilSaoPauloState):
    """Brazil São Paulo City"""

    FIXED_HOLIDAYS: Incomplete
    include_fat_tuesday: ClassVar[bool]
    fat_tuesday_label: ClassVar[str]
    include_easter_sunday: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_good_friday: ClassVar[bool]
    good_friday_label: ClassVar[str]
    include_consciencia_negra: ClassVar[bool]
    consciencia_negra_label: ClassVar[str]

class BrazilSergipe(Brazil):
    """Brazil Sergipe State"""

    FIXED_HOLIDAYS: Incomplete

class BrazilTocantins(Brazil):
    """Brazil Tocantins State"""

    FIXED_HOLIDAYS: Incomplete

class BrazilVitoriaCity(BrazilEspiritoSanto):
    """Brazil Vitória City"""

    FIXED_HOLIDAYS: Incomplete
    include_corpus_christi: ClassVar[bool]
    include_good_friday: ClassVar[bool]
    good_friday_label: ClassVar[str]

class BrazilVilaVelhaCity(BrazilEspiritoSanto):
    """Brazil Vila Velha City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilCariacicaCity(BrazilEspiritoSanto):
    """Brazil Cariacica City"""

    FIXED_HOLIDAYS: Incomplete
    include_corpus_christi: ClassVar[bool]
    include_good_friday: ClassVar[bool]
    good_friday_label: ClassVar[str]
    include_sao_joao: ClassVar[bool]
    sao_joao_label: ClassVar[str]

class BrazilGuarapariCity(BrazilEspiritoSanto):
    """Brazil Guarapari City"""

    FIXED_HOLIDAYS: Incomplete
    include_sao_pedro: ClassVar[bool]
    include_consciencia_negra: ClassVar[bool]
    consciencia_negra_day: Incomplete
    include_immaculate_conception: ClassVar[bool]

class BrazilSerraCity(BrazilEspiritoSanto):
    """Brazil Serra City"""

    FIXED_HOLIDAYS: Incomplete
    include_fat_tuesday: ClassVar[bool]
    fat_tuesday_label: ClassVar[str]
    include_ash_wednesday: ClassVar[bool]
    ash_wednesday_label: ClassVar[str]
    include_good_friday: ClassVar[bool]
    good_friday_label: ClassVar[str]
    include_sao_pedro: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]
    def get_variable_days(self, year): ...

class BrazilRioBrancoCity(BrazilAcre):
    """Brazil Rio Branco City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilMaceioCity(BrazilAlagoas):
    """Brazil Maceió City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilManausCity(BrazilAmazonas):
    """Brazil Manaus City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilMacapaCity(BrazilAmapa):
    """Brazil Macapá City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilSalvadorCity(BrazilBahia):
    """Brazil Salvador City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilFortalezaCity(BrazilCeara):
    """Brazil Fortaleza City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilGoianiaCity(BrazilGoias):
    """Brazil Goiânia City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilBeloHorizonteCity(BrazilMinasGerais):
    """Brazil Belo Horizonte City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilCampoGrandeCity(BrazilMatoGrossoDoSul):
    """Brazil Campo Grande City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilCuiabaCity(BrazilMatoGrosso):
    """Brazil Cuiabá City"""

    FIXED_HOLIDAYS: Incomplete
    include_easter_sunday: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_good_friday: ClassVar[bool]
    good_friday_label: ClassVar[str]

class BrazilBelemCity(BrazilPara):
    """Brazil Belém City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilJoaoPessoaCity(BrazilParaiba):
    """Brazil João Pessoa City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilRecifeCity(BrazilPernambuco):
    """Brazil Recife City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilTeresinaCity(BrazilPiaui):
    """Brazil Teresina City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilCuritibaCity(BrazilParana):
    """Brazil Curitiba City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilNatalCity(BrazilRioGrandeDoNorte):
    """Brazil Natal City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilPortoVelhoCity(BrazilRondonia):
    """Brazil Porto Velho City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilBoaVistaCity(BrazilRoraima):
    """Brazil Boa Vista City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilPortoAlegreCity(BrazilRioGrandeDoSul):
    """Brazil Porto Alegre City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilChapecoCity(BrazilSantaCatarina):
    """Brazil Chapecó City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilFlorianopolisCity(BrazilSantaCatarina):
    """Brazil Florianópolis City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilJoinvilleCity(BrazilSantaCatarina):
    """Brazil Joinville City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilAracajuCity(BrazilSergipe):
    """Brazil Aracaju City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilSorocabaCity(BrazilSaoPauloState):
    """Brazil Sorocaba City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilPalmasCity(BrazilTocantins):
    """Brazil Palmas City"""

    FIXED_HOLIDAYS: Incomplete

class BrazilBankCalendar(Brazil):
    """
    Calendar that considers only working days for bank transactions
    for companies and the general public
    """

    include_fat_tuesday: ClassVar[bool]
    fat_tuesday_label: ClassVar[str]
    include_good_friday: ClassVar[bool]
    include_ash_wednesday: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_easter_sunday: ClassVar[bool]
    def get_last_day_of_year_for_only_internal_bank_trans(self, year):
        """
        The last day of year isn't a working day for public bank
        transactions in Brazil. More details can be read in
        http://www.bcb.gov.br/pre/bc_atende/port/servicos4.asp
        """

    def get_variable_days(self, year):
        """
        Define the brazilian variable holidays and the last
        day for only internal bank transactions
        """

    def find_following_working_day(self, day):
        """
        Find for the next working day by ignoring weekends,
        fixed and non fixed holidays and the last working
        day for only internal bank transactions in Brazil
        """

IBGE_TUPLE: Incomplete
IBGE_REGISTER: Incomplete
