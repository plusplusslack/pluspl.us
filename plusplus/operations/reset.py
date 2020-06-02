import json


def generate_reset_block():
    sections = []
    # add info section
    sections.append({
      'type': 'section',
      'text': {
        'type': 'mrkdwn',
        'text': 'Click the button below to delete all pluspl.us items for this Slack team'
      }
    })

    # add button sections
    sections.append({
        'type': 'actions',
        'elements': [{
            'type': 'button',
            'text': {
                'type': 'plain_text',
                'text': 'Permanently Delete All Items'
            },
            'value': 'delete_all',
            'style': 'danger',
            'confirm': {
                'title': {
                    'type': 'plain_text',
                    'text': 'Are you sure?'
                },
                'text': {
                    'type': 'mrkdwn',
                    'text': ':warning: *Warning!* :warning: Clicking the button below will permanently erase all objects for your team. There is no way to undo this, so proceed cautiously.'  # noqa: E501
                },
                'confirm': {
                    'type': 'plain_text',
                    'text': 'Do it'
                },
                'deny': {
                    'type': 'plain_text',
                    'text': 'Stop, I\'ve changed my mind!'
                }
            }
        }]
    })
    return json.dumps(sections)
