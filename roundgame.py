from typing import *
from time import sleep

print(123)
class Player:
    
    def __init__ (self,
                 name : str,
                 current_hp : int ,
                 total_hp : int ,
                 skills : list[object] ,
                 buffs : Dict[object, int],
                 speed : int,
                 atk_v : int,
                 property_ : str,
                 enermy : object
                ) -> None :
        
        self.name = name
        self.current_hp = current_hp         
        self.total_hp = total_hp
        self.skills = skills
        self.buffs = buffs
        self.speed = speed
        self.atk_v = atk_v
        self.property_ = property_
        self.enermy = enermy
        
        
    def use_skills(self) -> None:
        
        chosen_skill = self.choose_skill()
        if chosen_skill.to_order_buff != 无:
            self.buffs[chosen_skill.to_order_buff] = chosen_skill.to_order_buff.round
        if chosen_skill.to_receiver_buff != 无:
            self.enermy.buffs[chosen_skill.to_receiver_buff] = chosen_skill.to_receiver_buff.round
        chosen_skill.refresh()
        print(chosen_skill.current_cd)
        self.return_final_damage(self.enermy,chosen_skill)
    
    
    def choose_skill(self) -> object:
    
        while True :
            ch = self.skills[int(input(f'{self.name} 选择技能'))]
            if ch.current_cd : print(f'{ch.name} 冷却中')
            else: break 
        return ch
    
    
    def show_info(self) -> None:
        sum = 0
        print(f'\t{self.name} {self.property_}属性 血量:{self.current_hp}/{self.total_hp}','|'*int((self.current_hp/self.total_hp)*50))
        print('\t\t技能列表')
        for ski in self.skills:
             print(f"\t\t{sum} {ski.name},{ski.current_cd}")
             sum += 1
             
        for buf in self.buffs:
            if buf.type_ in ('加攻', '减攻', '减伤'):
                print(f'\t\t{buf.name+str(buf.influence)} 回合数{self.buffs[buf]}')
            else: print(f'\t\t{buf.name} 回合数{self.buffs[buf]}')
            
        print('\n')
            
    
    def show_player_state(self) -> None:
        
        for _buff in self.buffs:
            if _buff.type_ == '控制':
                print(f'{self.name} 无法行动')
     
     
    def refresh_buffs_influence(self) -> None:
        
        for _buff in list(self.buffs):
            if _buff.type_ == '持续伤害': 
                self.current_hp -= _buff.influence
                print(f'{self.name}因灼烧 受到{_buff.influence}点伤害')
    
            
    def refresh_buffs(self) -> None:
        
        for _buff in list(self.buffs):
            if self.buffs[_buff]: 
                self.buffs[_buff] -= 1
                if not self.buffs[_buff]: del self.buffs[_buff]
                  
    
    def refresh(self) -> None:
        
        self.refresh_buffs_influence()
        self.refresh_buffs()
    
    
    def return_final_damage(self, receiver : object, skill : object) -> None:
    
        damage_add = 1
        for _buff in self.buffs :
            if _buff.type_ == '加攻': damage_add += _buff.influence
            if _buff.type_ == '减攻': damage_add += _buff.influence
    
        for _buff in receiver.buffs:
            if _buff.type_ == '减伤': damage_add += _buff.influence
            pass
        print(f'{receiver.name} 因 {skill.name} 受到{self.atk_v*damage_add*skill.basic_v} 点伤害')
        damage_add += compare_property(self, receiver)
        receiver.current_hp -= self.atk_v*damage_add*skill.basic_v

    
def compare_property(pla1: object, pla2: object) -> float:
    if (pla1.property_, pla2.property_) not in restrain_dict:
        return 0.0
    return restrain_dict[(pla1.property_, pla2.property_)]
            
    
class Skills:
    
    def __init__(self,
                 name : str,
                 current_cd : int,
                 use_cd : int,
                 state : Dict[object , int],
                 basic_v : float,
                 to_order_buff : object,
                 to_receiver_buff : object
                 ) -> None:
        
        self.name = name
        self.current_cd = current_cd
        self.use_cd = use_cd
        self.state = state
        self.basic_v = basic_v
        self.to_order_buff = to_order_buff
        self.to_receiver_buff = to_receiver_buff

    def refresh_skills_cd(self) -> None:
        if not self.current_cd:
            self.current_cd = self.use_cd


    def refreh_state(self) -> None:
        pass


    def refresh(self) -> None:
        self.refresh_skills_cd()  

            
class Buffs:
    
    def __init__(self,
                 name : str,
                 round : int,
                 type_ : str,
                 influence : int
                 ) -> None:
        
        self.name = name
        self.round = round
        self.type_ = type_
        self.influence = influence
        
        
class EventsManager:
    
    def __init__(self) -> None:
        self.events = []
        
        
    def add_events(self, event : object) -> None:
        self.events.append(event)
        
        
    @staticmethod
    def judge_event_run(event) -> bool:
        
        if not event.order.current_hp <= 0 :
            if not any(buff_.type_ == '控制' for buff_ in event.order.buffs):
                
                return True
        print(f'{event.order.name} 无法行动')    
        return False
    
        
    def refresh(self) -> Any :
        
        while self.events :
            eve = self.events.pop(0)
            #print(eve.order)
            if EventsManager.judge_event_run(eve):
                eve.func()
   
    def sort_events(self) -> None :
        pass

                    
class Events:
    
    def __init__(self, order : object, func : Any, receiver : object) -> None:
        
        self.order = order
        self.func = func
        self.receiver = receiver
            
    @staticmethod
    def create_new_event(order, func, receiver) -> object:
        global num
        num = (num + 1)%len(all_event)
        all_event[num].order = order
        all_event[num].func = func
        all_event[num].receiver = receiver
        return all_event[num]
        
        
def show_players_info(player_list) -> None:
    
    for players in player_list:
        sleep(0.5)
        players.show_info()    


def show_player_list(list : list) -> None:
    for player_ in Player_list:
        print(f'{Player_list.index(player_)} {player_.name} {player_.property_}')


def show_skill_list(list : list) -> None:
    for skill_ in skill_list:
        print(f'{skill_list.index(skill_)} {skill_.name}')


def create_player() -> None:
    
    print('角色列表')
    show_player_list(Player_list)
    print('技能列表')
    show_skill_list(skill_list) 
    player1 = Player_list.pop(int(input('选择角色1')))
    show_player_list(Player_list)
    player2 = Player_list.pop(int(input('选择角色2')))
    
    while len(player1.skills) < skill_limit:
        player1.skills.append(skill_list.pop(int(input('选择角色1技能'))))
        show_skill_list(skill_list)
    
    while len(player2.skills) < skill_limit:
        player2.skills.append(skill_list.pop(int(input('选择角色2技能'))))
        show_skill_list(skill_list)    
    player1.enermy = player2
    player2.enermy = player1
    return [player1,player2]


def main() -> None :
    player_list = create_player()
    round_ = 1
    show_players_info(player_list)
    while not any(player.current_hp <= 0 for player in player_list):
        print('\n'*10)
        print(f'回合{round_} 开始')
        for player in player_list:
            event = Events.create_new_event(player, player.use_skills, player.enermy)
            em.add_events(event)
            
        em.refresh()
        
        for player in player_list:
            event = Events.create_new_event(player, player.refresh, player.enermy)
            em.add_events(event)
            for _buff in list(player.buffs):
                if not player.buffs[_buff]: del player.buffs[_buff]
        print(f'回合{round_} 结束')
        
        em.refresh()
        show_players_info(player_list)
        round_ += 1    
        sleep(1)
            

# 创建时间管理器

em = EventsManager()     

""" 事件对象
 order : object, func : Any, receiver : object
"""

num = 0

eventA = Events(None,None,None)
eventB = Events(None,None,None)
eventC = Events(None,None,None)
eventD = Events(None,None,None)

all_event = [eventA, eventB, eventC, eventD]

""""角色
                 name : str,
                 current_hp : int ,
                 total_hp : int ,
                 skills : list[object] ,
                 buffs : Dict[object , int],
                 speed : int,
                 atk_v : int,
                 property_ : str,
                 enermy : object
                
                """
                
                
水蓝蓝 = Player('水蓝蓝', 500, 500, [], {}, 10, 100, '水',None )           
小火龙 = Player('小火龙', 500, 500, [], {}, 10, 100, '火',None )
水蓝蓝 = Player('水蓝蓝', 500, 500, [], {}, 10, 100, '水',None )
妙蛙种子 = Player('妙蛙种子', 500, 500, [], {},10, 100, '草', None)

Player_list = [小火龙,水蓝蓝]


"""buff
                 name : str,
                 round : int,
                 type_ : str,
                 influence : Any

                """
灼烧 = Buffs('灼烧', 3, '持续伤害',50 )

击飞 = Buffs('击飞', 0, '控制', 0)

无 = Buffs('无', 0, '无', 0)

湿润 = Buffs('加攻', 3, '加攻', 0.5)

减伤 = Buffs('减伤',1,'减伤',-0.8)

""" 技能
                 name : str,
                 current_cd : int,
                 use_cd : int,
                 state : Dict[object , int],
                 basic_v : float,
                 to_order_buff : object,
                 to_receiver_buff : object 
                 
                 """
skill_limit = 2
                 
                 
甩尾 = Skills('甩尾', 0, 0, {}, 1.5, 无,无 )

猛击 = Skills('猛击', 0, 0, {},1.5, 无, 无)

喷火 = Skills('喷火', 0, 2, {}, 0.8, 无, 灼烧 )

湿润 = Skills('湿润', 0, 2, {}, 0, 湿润, 无)

防御 = Skills('防御', 0, 0, {}, 0, 减伤, 无)

skill_list=[甩尾, 猛击, 喷火, 湿润, 防御]

"""克制关系
    水 -> 火
    火 -> 草
    草 -> 水
    
"""

restrain_dict = {('水','火') : 0.5, ('火','草') : 0.5, ('草','水') : 0.5}

if __name__ == '__main__' :
    main()
    
    
