let timer
let timeLeft = 60

const $guessForm = $('#guess-form')
const $foundWords = $('#words-found-list')
const $currentScore = $('#current-score')
let newScore = 0

const wordsFound = new Set()

const gameOver = async () => {
	clearInterval(timer)
	await addScore(parseInt($currentScore.text()))
	$('#play-again-button').show()
	$('#guess-form').hide()
	$('#guess-results').hide()
}

const updateTimer = () => {
	timeLeft = timeLeft - 1
	if (timeLeft >= 0) $('#timer').html(timeLeft)
	else {
		gameOver()
	}
}

const start = () => {
	timer = setInterval(updateTimer, 1000)
	updateTimer()
}

const checkGuess = async (evt) => {
	evt.preventDefault()
	const guess = $('#guess').val()
	const resp = await axios.get('/check-guess', {params: {guess: guess}})
	let responseResult = responseText(resp.data.result)

	if (responseResult === 'Awesome find') {
		if (!wordsFound.has(guess)) {
			//update score, add to list, add to DOM list
			newScore += guess.length
			$currentScore.text(newScore)
			wordsFound.add(guess)
			$foundWords.append(`<li>${guess}</li>`)
		} else {
			responseResult = 'That word has already been found!'
		}
	}

	$('#guess-results').text(responseResult)
	$('#guess').val('')
}

const responseText = (result) => {
	if (result === 'not-word') {
		return 'Not a valid word'
	} else if (result === 'not-on-board') {
		return 'Not on the board'
	} else {
		return 'Awesome find'
	}
}

$guessForm.on('submit', checkGuess)

const addScore = async (currentScore) => {
	const res = await axios.post('/add-score', {
		score : currentScore
	})
	let highscore = res.data.highscore
	$('#high-score').text(highscore)
}
