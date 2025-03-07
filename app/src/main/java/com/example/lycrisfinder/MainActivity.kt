package com.example.lycrisfinder

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Toast
import androidx.lifecycle.lifecycleScope
import com.google.android.material.button.MaterialButton
import com.google.android.material.textfield.TextInputEditText
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Query

// Data classes for API response
data class LyricsResponse(
    val status: String,
    val lyrics: String? = null,
    val message: String? = null
)

// Retrofit interface
interface LyricsApi {
    @GET("get_lyrics")
    suspend fun getLyrics(@Query("query") query: String): LyricsResponse
    
    @GET("get_lyrics")
    suspend fun getLyricsWithArtist(
        @Query("artist") artist: String,
        @Query("title") title: String
    ): LyricsResponse
}

class MainActivity : AppCompatActivity() {
    private lateinit var songInput: TextInputEditText
    private lateinit var searchButton: MaterialButton
    private lateinit var lyricsTextView: android.widget.TextView
    
    // Initialize Retrofit
    private val api = Retrofit.Builder()
        .baseUrl("https://lyricsfinder-api-uper.onrender.com/")
        .addConverterFactory(GsonConverterFactory.create())
        .build()
        .create(LyricsApi::class.java)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Initialize views
        songInput = findViewById(R.id.songInputEditText)
        searchButton = findViewById(R.id.searchButton)
        lyricsTextView = findViewById(R.id.lyricsTextView)

        // Set up click listener
        searchButton.setOnClickListener {
            val query = songInput.text.toString()
            if (query.isNotBlank()) {
                fetchLyrics(query)
            } else {
                Toast.makeText(this, "Please enter a song title or URL", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun fetchLyrics(query: String) {
        lifecycleScope.launch(Dispatchers.IO) {
            try {
                // Try Genius API first
                val parts = query.split("-")
                val response = if (parts.size == 2) {
                    val artist = parts[0].trim()
                    val title = parts[1].trim()
                    api.getLyricsWithArtist(artist, title)
                } else {
                    // Fallback to basic query
                    api.getLyrics(query)
                }

                withContext(Dispatchers.Main) {
                    when {
                        response.lyrics != null -> {
                            lyricsTextView.text = response.lyrics
                        }
                        response.message != null -> {
                            lyricsTextView.text = "Error: ${response.message}"
                        }
                        else -> {
                            lyricsTextView.text = "No lyrics found"
                        }
                    }
                    searchButton.isEnabled = true
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    lyricsTextView.text = "Error: ${e.message}"
                    searchButton.isEnabled = true
                }
            }
        }
    }
}
