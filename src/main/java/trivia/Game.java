package trivia;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

// REFACTOR ME
public class Game implements IGame {
   private static final int WINNING_COINS = 6;
   private static final int QUESTIONS_PER_CATEGORY = 50;
   private static final int BOARD_SIZE = 12;

   List<Player> players = new ArrayList<>();

   LinkedList popQuestions = new LinkedList();
   LinkedList scienceQuestions = new LinkedList();
   LinkedList sportsQuestions = new LinkedList();
   LinkedList rockQuestions = new LinkedList();

   int currentPlayer = 0;
   boolean isGettingOutOfPenaltyBox;

   public Game() {
      for (int i = 0; i < QUESTIONS_PER_CATEGORY; i++) {
         popQuestions.addLast("Pop Question " + i);
         scienceQuestions.addLast(("Science Question " + i));
         sportsQuestions.addLast(("Sports Question " + i));
         rockQuestions.addLast(createRockQuestion(i));
      }
   }

   public String createRockQuestion(int index) {
      return "Rock Question " + index;
   }

   public boolean hasEnoughPlayers() {
      return (howManyPlayers() >= 2);
   }

   public boolean add(String playerName) {
      players.add(new Player(playerName));

      System.out.println(playerName + " was added");
      System.out.println("They are player number " + players.size());
      return true;
   }

   public int howManyPlayers() {
      return players.size();
   }

   public void roll(int roll) {
      Player player = players.get(currentPlayer);
      System.out.println(player + " is the current player");
      System.out.println("They have rolled a " + roll);

      if (player.isInPenaltyBox()) {
         if (roll % 2 != 0) {
            isGettingOutOfPenaltyBox = true;

            System.out.println(player + " is getting out of the penalty box");
            player.setPosition(player.getPosition() + roll);
            if (player.getPosition() > BOARD_SIZE) player.setPosition(player.getPosition() - BOARD_SIZE);

            System.out.println(player
                               + "'s new location is "
                               + player.getPosition());
            System.out.println("The category is " + currentCategory());
            askQuestion();
         } else {
            System.out.println(player + " is not getting out of the penalty box");
            isGettingOutOfPenaltyBox = false;
         }

      } else {

         player.setPosition(player.getPosition() + roll);
         if (player.getPosition() > BOARD_SIZE) player.setPosition(player.getPosition() - BOARD_SIZE);

         System.out.println(player
                            + "'s new location is "
                            + player.getPosition());
         System.out.println("The category is " + currentCategory());
         askQuestion();
      }

   }

   private void askQuestion() {
      if (currentCategory() == "Pop")
         System.out.println(popQuestions.removeFirst());
      if (currentCategory() == "Science")
         System.out.println(scienceQuestions.removeFirst());
      if (currentCategory() == "Sports")
         System.out.println(sportsQuestions.removeFirst());
      if (currentCategory() == "Rock")
         System.out.println(rockQuestions.removeFirst());
   }


   private String currentCategory() {
      Player player = players.get(currentPlayer);
      if (player.getPosition() - 1 == 0) return "Pop";
      if (player.getPosition() - 1 == 4) return "Pop";
      if (player.getPosition() - 1 == 8) return "Pop";
      if (player.getPosition() - 1 == 1) return "Science";
      if (player.getPosition() - 1 == 5) return "Science";
      if (player.getPosition() - 1 == 9) return "Science";
      if (player.getPosition() - 1 == 2) return "Sports";
      if (player.getPosition() - 1 == 6) return "Sports";
      if (player.getPosition() - 1 == 10) return "Sports";
      return "Rock";
   }

   public boolean handleCorrectAnswer() {
      Player player = players.get(currentPlayer);
      if (player.isInPenaltyBox()) {
         if (isGettingOutOfPenaltyBox) {
            System.out.println("Answer was correct!!!!");
            player.addCoin();
            System.out.println(player
                               + " now has "
                               + player.getCoins()
                               + " Gold Coins.");

            boolean winner = !playerHasWon();
            currentPlayer++;
            if (currentPlayer == players.size()) currentPlayer = 0;

            return winner;
         } else {
            currentPlayer++;
            if (currentPlayer == players.size()) currentPlayer = 0;
            return true;
         }


      } else {

         System.out.println("Answer was corrent!!!!");
         player.addCoin();
         System.out.println(player
                            + " now has "
                            + player.getCoins()
                            + " Gold Coins.");

         boolean winner = !playerHasWon();
         currentPlayer++;
         if (currentPlayer == players.size()) currentPlayer = 0;

         return winner;
      }
   }

   public boolean wrongAnswer() {
      Player player = players.get(currentPlayer);
      System.out.println("Question was incorrectly answered");
      System.out.println(player + " was sent to the penalty box");
      player.setInPenaltyBox(true);

      currentPlayer++;
      if (currentPlayer == players.size()) currentPlayer = 0;
      return true;
   }


   private boolean playerHasWon() {
      return players.get(currentPlayer).getCoins() == WINNING_COINS;
   }
}
