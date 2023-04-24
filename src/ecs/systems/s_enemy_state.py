import esper

from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_transform import CTransform

def system_enemy_state(world: esper.World, player_entity: int, enemy_info: dict):
    pl_t = world.component_for_entity(player_entity, CTransform)
    components = world.get_components(CEnemyState, CVelocity, CAnimation, CTransform)
    for _, (c_est, c_v, c_a, c_t) in components:
        if c_est.state == EnemyState.IDLE:
            _do_idle_state(c_v, c_a, c_est, c_t, pl_t, enemy_info)
        elif c_est.state == EnemyState.MOVE:
            _do_move_state(c_v, c_a, c_est, c_t, pl_t, enemy_info)
        elif c_est.state == EnemyState.RETURN:
            _do_return_state(c_v, c_a, c_est, c_t, enemy_info)

def _do_idle_state(c_v: CVelocity, c_a: CAnimation,c_est: CEnemyState, c_t: CTransform, pl_t:CTransform, enemy_info:dict):
    _set_animation(c_a, 0)
    c_v.vel.x = 0
    c_v.vel.y = 0

    dist_to_player = c_t.pos.distance_to(pl_t.pos)
    if dist_to_player < enemy_info["distance_start_chase"]:
        c_est.state = EnemyState.MOVE


def _do_move_state(c_v: CVelocity, c_a: CAnimation, c_est: CEnemyState, c_t: CTransform, pl_t:CTransform, enemy_info:dict):
    _set_animation(c_a, 1)
    c_v.vel = (pl_t.pos - c_t.pos).normalize() * enemy_info["velocity_chase"]
    distance_to_origin = c_est.start_pos.distance_to(c_t.pos)
    if distance_to_origin >= enemy_info["distance_start_return"]:
        c_est.state = EnemyState.RETURN

def _do_return_state(c_v: CVelocity, c_a: CAnimation, c_est: CEnemyState, c_t: CTransform, enemy_info:dict):
    _set_animation(c_a, 1)
    c_v.vel = (c_est.start_pos - c_t.pos).normalize() * enemy_info["velocity_return"]
    distance_to_origin = c_est.start_pos.distance_to(c_t.pos)
    if distance_to_origin <= 2:
        c_t.pos.xy = c_est.start_pos.xy
        c_est.state = EnemyState.IDLE

def _set_animation(c_a: CAnimation, num_anim:int):
    if c_a.current_animation == num_anim:
        return
    c_a.current_animation = num_anim
    c_a.current_animation_time = 0
    c_a.current_frame = c_a.current_frame = c_a.animations_list[c_a.current_animation].start
