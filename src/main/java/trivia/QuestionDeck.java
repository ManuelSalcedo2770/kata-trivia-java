package trivia;

import java.util.LinkedList;

public class QuestionDeck {

    private static final int QUESTIONS_PER_CATEGORY = 50;

    private final LinkedList<String> popQuestions = new LinkedList<>();
    private final LinkedList<String> scienceQuestions = new LinkedList<>();
    private final LinkedList<String> sportsQuestions = new LinkedList<>();
    private final LinkedList<String> rockQuestions = new LinkedList<>();
    private final LinkedList<String> geographyQuestions = new LinkedList<>();

    public QuestionDeck() {
        for (int i = 0; i < QUESTIONS_PER_CATEGORY; i++) {
            popQuestions.addLast("Pop Question " + i);
            scienceQuestions.addLast("Science Question " + i);
            sportsQuestions.addLast("Sports Question " + i);
            rockQuestions.addLast("Rock Question " + i);
            geographyQuestions.addLast("Geography Question " + i);
        }
    }

    public String nextQuestion(String category) {
        switch (category) {
            case "Pop":       return popQuestions.removeFirst();
            case "Science":   return scienceQuestions.removeFirst();
            case "Sports":    return sportsQuestions.removeFirst();
            case "Geography": return geographyQuestions.removeFirst();
            default:          return rockQuestions.removeFirst();
        }
    }
}
