from Action import Action
class Conference(Action):
	def __init__(self):
		Action.__init__(self, tag="Conference")
		
class Dial(Action):
	def __init__(self, phoneNumbers, record=None, sequential=None, callerId=None, ringBackTone=None, maxDuration=None):
		phoneNumbers = '"' + phoneNumbers + '"'
		attributes = {'phoneNumbers': phoneNumbers}
		if record is not None:
			record = '"' + record + '"'
			attributes['record'] = record
		if sequential is not None:
			sequential= '"' + sequential + '"'
			attributes['sequential'] = sequential
		if callerId is not None:
			callerId= '"' + callerId + '"'
			attributes['callerId'] = callerId
		if ringBackTone is not None:
			ringBackTone = '"' + ringBackTone + '"'
			attributes['ringBackTone'] = ringBackTone
		if maxDuration is not None:
			maxDuration = '"' + maxDuration + '"'
			attributes['maxDuration'] = maxDuration
		Action.__init__(self, tag="Dial", attributes=attributes)

class Enqueue(Action):
	def __init__(self, name=None, holdMusic=None):
		attributes = {}
		if name is not None:
			name = '"' + name + '"'
			attributes['name'] = name
		if holdMusic is not None:
			holdMusic = '"' + holdMusic + '"'
			attributes['holdMusic'] = holdMusic
		Action.__init__(self, tag="Enqueue", attributes=attributes)

class Dequeue(Action):
	def __init__(self, phoneNumber):
		phoneNumber = '"' + phoneNumber + '"'
		attributes = {'phoneNumber': phoneNumber}
		Action.__init__(self, tag="Dequeue", attributes=attributes)

class GetDigits(Action):
	def __init__(self, say = None, play=None, numDigits=None, timeout="30", finishOnKey=None, callbackUrl=None):
		children = []
		attributes = {}
		if say is not None:
			children.append(say)
		if play is not None:
			children.append(play)
		if numDigits is not None:
			numDigits = '"' + numDigits + '"'
			attributes['numDigits'] = numDigits
		if timeout is not None:
			timeout = '"' + timeout + '"'
			attributes['timeout'] = timeout
		if finishOnKey is not None:
			finishOnKey = '"' + finishOnKey + '"'
			attributes['finishOnKey'] = finishOnKey
		if callbackUrl is not None:
			callbackUrl = '"' + callbackUrl + '"'
			attributes['callBackUrl'] = callbackUrl
		Action.__init__(self, tag= "GetDigits", children = children, attributes = attributes)

class Play(Action):
	def __init__(self, url):
		url = '"' + url + '"'
		attributes = {'url':url}
		Action.__init__(self, "Play", attributes = attributes)

class Record(Action):
	def __init__(self, say=None, play=None, finishOnKey=None, maxLength=None, timeout=None, trimSilence=None, playBeep=None, callbackUrl=None):
		children = []
		attributes ={}
		if say is not None:
			children.append(say)
		if play is not None:
			children.append(play)
		if maxLength is not None:
			maxLength = '"' + maxLength + '"'
			attributes['maxLength'] = maxLength
		if timeout is not None:
			timeout = '"' + timeout + '"'
			attributes['timeout'] = timeout
		if finishOnKey is not None:
			finishOnKey = '"' + finishOnKey + '"'
			attributes['finishOnKey'] = finishOnKey
		if callbackUrl is not None:
			callbackUrl = '"' + callbackUrl + '"'
			attributes['callBackUrl'] = callbackUrl
		if playBeep is not None:
			playBeep = '"' + playBeep + '"'
			attributes['playBeep'] = playBeep
		if trimSilence is not None:
			trimSilence = '"' + trimSilence + '"'
			attributes['trimSilence'] = trimSilence

		Action.__init__(self, tag="Record", children=children, attributes=attributes)

class Redirect(Action):
	def __init__(self, url):
		Action.__init__(self, tag="Redirect", text=url)

class Reject(Action):
	def __init__(self):
		Action.__init__(self, tag="Reject")

class Say(Action):
	def __init__(self, text, voice=None, playBeep=None):
		attributes={}
		if voice is not None:
			voice = '"' + voice + '"'
			attributes['voice'] = voice
		if playBeep is not None:
			playBeep = '"' + playBeep + '"'
			attributes['playBeep'] = playBeep
		Action.__init__(self, tag = "Say", text = text, attributes = attributes)
