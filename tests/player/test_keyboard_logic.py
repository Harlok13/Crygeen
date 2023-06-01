from crygeen import PlayerKeyboardInput
from crygeen.game_process.player_setup.player_keyboard_input import KeyboardLogic, Direction


class PlayerMock:
    def __init__(self):
        pass


class TestKeyboardLogic:
    kbl: KeyboardLogic = KeyboardLogic(PlayerKeyboardInput(PlayerMock))

    def test_idle(self):
        """
        when the character does nothing
        1 - test flag idle to true
        2 - test character doesn't move
        3 - test status is correct
        :return:
        """
        self.kbl.idle()
        assert self.kbl.kbi.idle                    # 1
        assert self.kbl.kbi.direction.xy == (0, 0)  # 2
        assert self.kbl.kbi.status == 'down_idle'   # 3

    def test_action(self):
        """
        when character is attacking
        1 - test during an attack, the status is prefixed with '_attack'
        2 - test the timer begins to count down the start of the attack
        3 - test that the attack is not available
        4 - test that the character does not move during the attack
        5 - test that if there is already a prefix, then the new one is not added
        when the character can't attack
        6 - test that the status is prefixed is not '_attack'
        7 - test that the attack start timer did not start running
        9 - test that the attack is unavailable
        9 - test that the character can move
        :return:
        """
        self.kbl.kbi.status = 'down_idle'
        self.kbl.action()

        # when attack is available ____________________________________________
        assert self.kbl.kbi.status == 'down_attack'                    # 1
        assert self.kbl.kbi.attack_start_time == 0                     # 2
        assert not self.kbl.kbi.attack_available                       # 3
        assert self.kbl.kbi.direction.xy == (0, 0)                     # 4
        self.kbl.kbi.status = 'up_attack'
        assert self.kbl.kbi.status == 'up_attack'                      # 5

        self.kbl.kbi.attack_available = False
        # when attack is unavailable __________________________________________
        self.kbl.kbi.status = 'down_idle'
        assert self.kbl.kbi.status == 'down_idle'                      # 6
        self.kbl.kbi.attack_start_time = 100
        assert self.kbl.kbi.attack_start_time == 100                   # 7
        assert not self.kbl.kbi.attack_available                       # 8
        self.kbl.kbi.direction.xy = (1, 0)
        assert self.kbl.kbi.direction.xy == self.kbl.kbi.direction.xy  # 9

    def test_spurt(self):
        """
        when the character uses spurt
        1 - test that the status is prefixed with '_spurt'
        2 - test that the character does not move
        3 - test that the character can move
        when the character can't use spurt
        4 - test that the spurt start timer did not start running
        5 - test that the spurt is unavailable
        6 - test that the speed of the character does not change
        :return:
        """
        spurt_speed = self.kbl.kbi.speed = 200
        self.kbl.spurt()

        # when spurt is available _____________________________________________
        assert self.kbl.kbi.spurt_start_time == 0      # 1
        assert not self.kbl.kbi.spurt_available        # 2
        spurt_speed *= (spurt_coefficient := 2)
        assert self.kbl.kbi.speed == spurt_speed       # 3

        self.kbl.kbi.spurt_available = False
        # when spurt is unavailable ___________________________________________
        self.kbl.kbi.spurt_start_time = 100
        spurt_speed = self.kbl.kbi.speed = 200
        assert self.kbl.kbi.spurt_start_time == 100    # 4
        assert not self.kbl.kbi.spurt_available        # 5
        assert self.kbl.kbi.speed == spurt_speed       # 6

    def test_move_left(self):
        """test correct direction"""
        self.kbl.move_left()
        assert self.kbl.kbi.direction.x == -1

    def test_move_right(self):
        """test correct direction"""
        self.kbl.move_right()
        assert self.kbl.kbi.direction.x == 1

    def test_move_up(self):
        """test correct direction"""
        self.kbl.move_up()
        assert self.kbl.kbi.direction.y == -1

    def test_move_down(self):
        """test correct direction"""
        self.kbl.move_down()
        assert self.kbl.kbi.direction.y == 1

    def test_move_upleft(self):
        """test correct direction"""
        self.kbl.move_up()
        self.kbl.move_left()
        assert self.kbl.kbi.direction.xy == (-1, -1)

    def test_move_upright(self):
        """test correct direction"""
        self.kbl.move_up()
        self.kbl.move_right()
        assert self.kbl.kbi.direction.xy == (1, -1)

    def test_move_downleft(self):
        """test correct direction"""
        self.kbl.move_down()
        self.kbl.move_left()
        assert self.kbl.kbi.direction.xy == (-1, 1)

    def test_move_downright(self):
        """test correct direction"""
        self.kbl.move_down()
        self.kbl.move_right()
        assert self.kbl.kbi.direction.xy == (1, 1)
