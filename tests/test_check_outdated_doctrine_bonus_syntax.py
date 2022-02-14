##########################
# Test script to check if doctrines are used in 'add_tech_bonus' expression - with NSB they have separate syntax
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from .imports.file_functions import open_text_file
import logging


def test_check_outdated_doctrine_bonus_syntax(test_runner: object):
    naval_doctrines = ['fleet_in_being', 'battlefleet_concentration', 'subsidiary_carrier_role', 'hunter_killer_groups',
                       'floating_fortress', 'floating_airfield', 'grand_battlefleet', 'convoy_sailing', 'convoy_escorts', 'escort_carriers',
                       'integrated_convoy_defence', 'submarine_operations', 'undersea_blockade', 'convoy_interdiction', 'submarine_offensive',
                       'trade_interdiction', 'convoy_interdiction_ti', 'unrestricted_submarine_warfare', 'wolfpacks', 'advanced_submarine_warfare',
                       'combined_operations_raiding', 'raider_patrols', 'capital_ship_raiders', 'battlefleet_concentration_ti', 'floating_fortress_ti',
                       'floating_airfield_ti', 'carrier_operations', 'convoy_sailing_ti', 'subsidiary_carrier_role_ti', 'naval_air_operations', 'base_strike',
                       'carrier_primacy', 'carrier_task_forces', 'floating_airfield_bs', 'massed_strikes', 'floating_fortress_bs', 'carrier_battlegroups',
                       'submarine_operations_bs', 'undersea_blockade_bs', 'convoy_interdiction_bs', 'submarine_offensive_bs', 'convoy_escorts_bs', 'escort_patrols',
                       'convoy_sailing_bs', 'integrated_convoy_defence_bs']

    air_doctrines = ['air_superiority', 'infrastructure_destruction', 'home_defence', 'naval_strike_tactics', 'fighter_sweeps',
                     'dogfighting_experience', 'multialtitude_flying', 'logistical_bombing', 'night_bombing', 'day_bombing', 'massed_bomber_formations',
                     'air_offense', 'flying_fortress', 'offensive_formations', 'mass_destruction', 'formation_flying', 'dive_bombing', 'direct_ground_support',
                     'formation_fighting', 'fighter_ace_initiative', 'hunt_and_destroy', 'combat_unit_destruction', 'battlefield_support', 'keypoint_bombing',
                     'ground_support_integration', 'naval_strike_torpedo_tactics', 'strategic_destruction', 'forward_interception', 'force_rotation', 'fighter_baiting',
                     'low_echelon_support', 'dispersed_fighting', 'operational_destruction', 'fighter_veteran_initiative', 'naval_strike_torpedo_tactics_oi', 'cas_veteran_initiative',
                     'carousel_bombing', 'infiltration_bombing', 'air_skirmish', 'high_level_bombing']

    land_doctrines = ['mobile_warfare', 'delay', 'elastic_defence', 'mobile_infantry', 'mass_motorization', 'mechanised_offensive', 'armored_spearhead',
                      'schwerpunk', 'blitzkrieg', 'kampfgruppe', 'firebrigades', 'backhand_blow', 'modern_blitzkrieg', 'volkssturm', 'nd_conscription', 'werwolf_guerillas',
                      'superior_firepower', 'sup_delay', 'mobile_defence', 'intergrated_support', 'regimental_combat_teams', 'dispersed_support', 'overwhelming_firepower',
                      'sup_mechanized_offensive', 'concentrated_fire_plans', 'combined_arms', 'tactical_control', 'air_land_battle', 'centralized_fire_control', 'forward_observers',
                      'advanced_firebases', 'shock_and_awe', 'trench_warfare', 'grand_battle_plan', 'prepared_defense', 'grand_assault', 'grand_mechanized_offensive', 'assault_concentration',
                      'branch_interoperation', 'assault_breakthrough', 'central_planning', 'c3i_theory', 'infantry_offensive', 'armored_operations', 'infiltration_assault', 'night_assault_tactics',
                      'attritional_containment', 'infiltration_in_depth', 'mass_assault', 'pocket_defence', 'defence_in_depth', 'large_front_operations', 'deep_operations',
                      'operational_concentration', 'vast_offensives', 'breakthrough_priority', 'mechanized_wave', 'continuous_offensive', 'peoples_army', 'human_infantry_offensive',
                                    'large_front_offensive', 'human_wave_offensive', 'guerilla_warfare', 'masterful_blitz']

    doctrine_categories = ['cat_mobile_warfare',
                           'cat_superior_firepower',
                           'cat_grand_battle_plan',
                           'cat_mass_assault',
                           'cat_base_strike',
                           'cat_trade_interdiction',
                           'cat_fleet_in_being',
                           'cat_strategic_destruction',
                           'cat_battlefield_support',
                           'cat_operational_integrity',
                           'capital_ship_tree',
                           'carrier_ship_tree',
                           'land_doctrine',
                           'air_doctrine',
                           'naval_doctrine',
                           'strategic_destruction_tree',
                           'battlefield_support_tree',
                           'operational_integrity_tree',
                           'trade_interdiction_tree',
                           'convoy_defense_tree',
                           'fleet_in_being_tree', ]

    combined_techs_list = naval_doctrines + \
        air_doctrines + land_doctrines + doctrine_categories

    filepath = test_runner.full_path_to_mod
    all_tech_bonuses = []
    results = []
    paths = {}
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = open_text_file(filename)

# Get all tech bonuses from mod files
        if 'add_tech_bonus =' in text_file:
            tech_bonuses_in_file = re.findall('add_tech_bonus = \\{[ \\w\r\n\t=.]*\\}', text_file)
            if len(tech_bonuses_in_file) > 0:
                for expression in tech_bonuses_in_file:
                    all_tech_bonuses.append(expression)
                    paths[expression] = os.path.basename(filename)

# Verify if doctrines/doctrine categories are used in the tech files
    for expression in all_tech_bonuses:
        for tech_name in combined_techs_list:
            if f'category = {tech_name}' in expression:
                results.append(f'{tech_name} doctrine/doctrine category is used in the following expression: \n{expression}')
            if f'technology = {tech_name}' in expression:
                results.append(f'{tech_name} doctrine/doctrine category is used in the following expression: \n{expression}')

    if results != []:
        for i in results:
            logging.error(f"- [ ] {i}, - '{paths[i]}'")
        logging.warning(f'{len(results)} times wrong doctrine syntax is used!')
        raise AssertionError("'Outdated doctrine bonus syntax encountered! Check console output")
