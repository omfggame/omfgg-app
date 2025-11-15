"""
Test constrained prompts to ensure simpler game designs
"""
import asyncio
from agents import CharacterAgent, MechanicAgent, StyleAgent, LevelAgent, TwistAgent, ComposerAgent
import json

async def test_constrained_prompts():
    print('Testing CONSTRAINED prompts with same inputs that caused issues...\n')
    print('='*60)

    # Same inputs that caused the ambitious output
    inputs = {
        'subject': 'pickle',
        'action': 'dancing',
        'vibe': 'Motley Python',
        'setting': 'Santas Workshop',
        'twist': "It's easter"
    }
    mode = 'Funny'
    provider = 'openai'

    print(f'Inputs: {inputs}')
    print(f'Mode: {mode}\n')

    # Create agents
    character = CharacterAgent()
    mechanic = MechanicAgent()
    style = StyleAgent()
    level = LevelAgent()
    twist = TwistAgent()
    composer = ComposerAgent()

    print('Running sub-agents in parallel...\n')

    # Run sub-agents
    results = await asyncio.gather(
        character.generate(inputs['subject'], mode, provider),
        mechanic.generate(inputs['action'], mode, provider),
        style.generate(inputs['vibe'], mode, provider),
        level.generate(inputs['setting'], mode, provider),
        twist.generate(inputs['twist'], mode, provider)
    )

    sub_agent_outputs = {
        'character': results[0],
        'mechanic': results[1],
        'style': results[2],
        'level': results[3],
        'twist': results[4]
    }

    print('Sub-agents complete!\n')
    print('='*60)
    print('TWIST AGENT OUTPUT (the one that was too ambitious):')
    print('='*60)
    print(results[4])
    print()

    print('='*60)
    print('Running Composer with Claude Sonnet 4.5...\n')

    game_def = composer.compose(mode, sub_agent_outputs)

    print('='*60)
    print('FINAL GAMEDEF:')
    print('='*60)
    print(game_def)
    print()

    # Try to extract just the special/twist section from GameDef
    try:
        # Try to parse as JSON
        if '```json' in game_def:
            json_str = game_def.split('```json')[1].split('```')[0]
        elif '```' in game_def:
            json_str = game_def.split('```')[1].split('```')[0]
        else:
            json_str = game_def

        game_obj = json.loads(json_str)
        if 'special' in game_obj:
            print('='*60)
            print('SPECIAL/TWIST SECTION IN FINAL GAMEDEF:')
            print('='*60)
            print(json.dumps(game_obj['special'], indent=2))
            print()

        if 'mechanics' in game_obj:
            print('='*60)
            print('MECHANICS SECTION (should be ONE simple interaction):')
            print('='*60)
            print(json.dumps(game_obj['mechanics'], indent=2))
            print()
    except Exception as e:
        print(f'Could not parse JSON: {e}')

if __name__ == "__main__":
    asyncio.run(test_constrained_prompts())
